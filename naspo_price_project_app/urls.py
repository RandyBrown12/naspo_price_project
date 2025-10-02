from django.contrib import admin
from django.urls import include, path

from naspo_price_project_app.views import homepage

urlpatterns = [
    path('', homepage, name='home'),
    path('', include('django_prometheus.urls')),
]