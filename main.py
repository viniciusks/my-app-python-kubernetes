# -*- coding: UTF-8 -*-
# Imports
import json
import tornado.ioloop
import tornado.web
import tornado.template
from bson.json_util import dumps
from bson.json_util import loads
from bson import json_util

# Import Redis
from redis import Redis
r = Redis(host='redis', port=6379, db=0)
#r = Redis(host='localhost', port=6379, db=0)

# Import ElasticSearch
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Import PyMongo
from pymongo import MongoClient
#client = MongoClient('mongo', 27017)
#client = MongoClient('localhost', 27017)

## -- CONEXÃO COM O MONGO DENTRO DO KUBERNETES -- ##
uri = "mongodb://mongo-0.mongo:27017,mongo-1.mongo:27017,mongo-2.mongo:27017"
client = MongoClient(uri)
## ---------------------------------------------- ##

# Database do MongoDB
db = client['my_app']
# Collections do MongoDB
users = db.users
products = db.products

# -- FLAGS -- #
flag_sync = False
flag_redis = False

# -- FUNÇÕES -- #

# Função que sincroniza os dados do MongoDB e do Elasticsearch
def sync_mes(database,index_param,type_param):
    dados = database.find({},{"_id": False})
    
    for dado in dados:
        json_info = json.dumps(dado)
        r.set(dado['name'], json_info)
        res = es.index(index=index_param,doc_type=type_param,id=dado['mongo_id'],body=dado)
    if res == {}:
        flag_sync = False
    else:
        flag_sync = True
        
    return flag_sync
    
# -- CLASSES -- #

class DefaultHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.set_header("Content-Type","application/json")
        self.content_type = "application/json"

    def ResponseWithJson(self,return_code,est_json):
        self.write(json.dumps({"return_code": return_code, "data": est_json}, default=json_util.default))



# -- AMBIENTE DE TESTES -- #

from modules import test

class Test(DefaultHandler):
    def get(self,id_test):
        
        if id_test == "1":
            res = test.TestConnectionMongoDB(users)
        elif id_test == "2":
            res = test.TestConnectionRedis(r)
        else:
            res = test.TestConnectionElasticsearch(es)

        self.ResponseWithJson(1,res)

# -- FIM -- #



class Home(tornado.web.RequestHandler):
    def get(self):
        #self.ResponseWithJson(1,"Entrou!")
        self.render("views/home.html")

class Insert(DefaultHandler):
    def post(self,idBusca):
        r.flushall()
        # Class generalizada, insere informação a qualquer DB se passar no "if" as configurações corretas
        # "idBusca" serve para verificar em qual banco de dados se deseja mexer
        # Faz a verificação de qual DB será o alvo
        if idBusca == "users":
            database = users
            index_search = "users"
            type_search = "user"
            field_search = "name"
            dados = database.find()
            idEs = dados.count() + 1
            name = self.get_argument("name","")
            email = self.get_argument("email","")
            info = {
                "mongo_id": idEs,
                "name": name,
                "email": email
            }

        elif idBusca == "products":
            database = products
            index_search = "products"
            type_search = "product"
            field_search = "name"
            dados = database.find()
            idEs = dados.count() + 1
            name = self.get_argument("name","")
            type_product = self.get_argument("type","")
            model = self.get_argument("model","")
            status = self.get_argument("status","")
            info = {
                "mongo_id": idEs,
                "name": name,
                "type": type_product,
                "model": model,
                "status": status
            }
        
        # Insere caso não tenha nada dentro do MongoDB
        if dados.count() == 0:
            database.insert(info)
            info = database.find_one({"name": info['name']}, {"_id": False})
            flag_sync = sync_mes(database,index_search,type_search)
            if flag_sync == True:
                flag_sync = False
                self.ResponseWithJson(1,info)
            else:
                self.ResponseWithJson(0,"Falha na sincronização com elasticsearch.")
        else:
            # Busca no ElasticSearch
            search = es.search(index=index_search, body={"query": {"match": {field_search: info[field_search]}}})
            hits = search['hits']['hits']
            # Busca no MongoDB com o resultado do ElasticSearch
            one_thing = {}
            for hit in hits:
                one_thing = database.find_one({field_search: hit['_source'][field_search]})
            # Se não tiver um resultado o find_one, o dado é inserido dentro do MongoDB
            if one_thing == {}:
                database.insert(info)
                info = database.find_one({"name": info['name']}, {"_id": False})
                flag_sync = sync_mes(database,index_search,type_search)
                if flag_sync == True:
                    flag_sync = False
                    self.ResponseWithJson(1,info)
                else:
                    self.ResponseWithJson(0,"Falha na sincronização com elasticsearch.")
            # Se tiver um resultado, o dado não é inserido
            else:
                self.ResponseWithJson(0,"Dados já existentes em nosso banco de dados.")

class Search(DefaultHandler):
    def post(self,idBusca):
        if idBusca == "users":
            database = users
            index_search = "users"
            field_search = "name"
        elif idBusca == "products":
            database = products
            index_search = "products"
            field_search = "name"
        
        search_list = []
        name = self.get_argument("name","")

        # Caso o name venha vazio, o elasticsearch busca todas as informações
        if name == "":
            # Procura todas as informações no Elastic
            search = es.search(index=index_search, body={"query": {"match_all": {}}})
            hits = search['hits']['hits']
            for hit in hits:
                flag_redis = r.exists(hit['_source'][field_search])
                if flag_redis == False:
                    one_search = database.find_one({field_search: hit['_source'][field_search]},{"_id": False})
                    search_list.append(one_search)
                else:
                    one_redis = json.loads(r.get(hit['_source'][field_search]).decode('utf-8'))
                    search_list.append(one_redis)
        # Caso "name" venha preenchido, o elasticsearch busca a informação referente ao "name"
        else:
            search = es.search(index=index_search, body={"query": {"match": {field_search: name}}})
            hits = search['hits']['hits']
            for hit in hits:
                flag_redis = r.exists(hit['_source'][field_search])
                if flag_redis == False:
                    one_search = database.find_one({field_search: hit['_source'][field_search]},{"_id": False})
                    search_list.append(one_search)
                else:
                    one_redis = json.loads(r.get(hit['_source'][field_search]).decode('utf-8'))
                    search_list.append(one_redis)
        
        if search_list == []:
            self.ResponseWithJson(0,"Nenhuma informação encontrada.")
            return
        self.ResponseWithJson(1,search_list)

class Teste(DefaultHandler):
    def get(self):
        teste = r.hgetall("vinicius")
        print(teste)



def make_app():
    return tornado.web.Application([
        (r"/", Home),
        (r"/insert/(.*)", Insert),
        (r"/search/(.*)", Search),
        (r"/test/(.*)", Test),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8081)
    tornado.ioloop.IOLoop.current().start()