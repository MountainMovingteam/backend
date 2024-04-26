from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("person", views.person),
    path("group", views.group),
    path("getInfo", views.get_info)
]
