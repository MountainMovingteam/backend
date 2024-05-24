from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("person", views.person),
    path("group", views.group),
    path("getInfo", views.get_info),
    path("init/place", views.init_place),
    path("reset/place", views.clear_place),
    path("delete", views.delete_order)
]
