FROM python:3

# Criando a pasta da aplicação
ADD . /

# Instalando dependencias da aplicação
RUN pip3 install tornado pymongo redis elasticsearch

EXPOSE 8081

CMD ["python3","main.py"]