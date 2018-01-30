#!/usr/bin/env bash

# Construir a imagem docker
cd docker/
docker build -t my_app .
docker login
viniciusks13
Vinicius@12
docker tag my_app viniciusks13/my_app
docker push viniciusks13/my_app

# Pegando imagem docker
eval $(minikube docker-env)
docker pull viniciusks13/my_app
kubectl set image deployments/my-app my-app=viniciusks13/my_app