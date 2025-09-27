from django.contrib import admin
from django.urls import path

from naspo_price_project_app.views import homepage

urlpatterns = [
    path('', homepage, name='home'),
]