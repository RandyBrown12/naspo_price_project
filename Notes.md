docker build . -f Dockerfile.Django -t randybrown12/naspo-django-app:latest;
docker push randybrown12/naspo-django-app:latest;
docker build . -f Dockerfile.nginx -t randybrown12/nginx-for-naspo-django-app:latest;
docker push randybrown12/nginx-for-naspo-django-app:latest;

kubectl delete -f Kubernetes/;
kubectl apply -f Kubernetes/;

["naspo-django-app"]

WyJuYXNwby1kamFuZ28tYXBwIl0=

["localhost"]

WyJsb2NhbGhvc3QiXQ==

gunicorn naspo_price_project.wsgi:application --bind 0.0.0.0:8000
