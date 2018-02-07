kubectl delete deploy elasticsearch && kubectl delete svc elasticsearch && kubectl delete serviceaccount elasticsearch
kubectl delete deployment redis && kubectl delete svc redis && kubectl delete configmap example-redis-config
kubectl delete persistentvolumeclaim mongo-persistent-storage-mongo-0 && kubectl delete persistentvolumeclaim mongo-persistent-storage-mongo-1 && kubectl delete persistentvolumeclaim mongo-persistent-storage-mongo-2 && kubectl delete statefulset mongo && kubectl delete svc mongo
