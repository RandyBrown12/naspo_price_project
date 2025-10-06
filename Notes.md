docker build . -f Dockerfile.Django -t randybrown12/naspo-django-app:latest;
docker push randybrown12/naspo-django-app:latest;
docker build . -f Dockerfile.nginx -t randybrown12/nginx-for-naspo-django-app:latest;
docker push randybrown12/nginx-for-naspo-django-app:latest;

kubectl delete -f Kubernetes/;
kubectl apply -f Kubernetes/;
kubectl delete -f Kubernetes/Prometheus;
kubectl apply -f Kubernetes/Prometheus;

helm install loki grafana/loki -n monitoring -f ./Kubernetes/Loki/Loki_config.yaml

helm install alloy grafana/alloy -f ./Kubernetes/Loki/Alloy_config.yaml -n monitoring

curl -H "Authorization: Bearer test_token_123" https://naspo-django-app-service.default.svc.cluster.local:443/metrics -k -v
