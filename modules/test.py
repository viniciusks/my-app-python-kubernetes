from redis import Redis
from pymongo import MongoClient
from elasticsearch import Elasticsearch

def TestConnectionMongoDB(collection):
    dados = collection.find({},{"_id": False})
    list_of_data = []
    for dado in dados:
        list_of_data.append(dado)
    return list_of_data

def TestConnectionRedis(redis):
    redis.set("test","hello world")
    r = redis.get("test")
    return r

def TestConnectionElasticsearch(elastic):
    json_test = {
        "test": "Hello Elasticsearch!"
    }
    elastic.index(index="test",doc_type="test",body=json_test)
    search = elastic.search(index="test", body={"query": {"match_all": {}}})
    return search