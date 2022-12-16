#! /bin/sh

microk8s stop
microk8s start

sleep 2
kubectl get nodes
kubectl get pods

#Apply the deployement for the web portal
kubectl apply -f ./web/web-portal_deployment.yaml

#Apply the service for the web portal
kubectl apply -f ./web/web-portal_service.yaml
