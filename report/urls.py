
from django.contrib import admin
from django.urls import path, include
from .views import generate_report

urlpatterns = [
    path("", generate_report, name='generate_report'),
]
