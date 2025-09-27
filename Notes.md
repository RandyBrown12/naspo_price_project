docker build . -f Dockerfile.Django -t randybrown12/naspo-django-app:latest;
docker push randybrown12/naspo-django-app:latest;


kubectl delete -f Kubernetes/

kubectl apply -f Kubernetes/EnvironmentVariables.yaml -f Kubernetes/Postgres.yaml -f Kubernetes/Django-app.yaml
