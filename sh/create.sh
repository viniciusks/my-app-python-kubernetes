kubectl create -f kube/deploy-elastic.yaml
kubectl create -f kube/deploy-redis.yaml
kubectl create -f kube/deploy-my-app.yaml
kubectl create -f kube/deploy-jenkins.yaml
kubectl create -f kube/stfulset-mongo.yaml
kubectl get all