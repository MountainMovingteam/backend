from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("search", views.search),
    path("search/details", views.details),
    path("search/details/group", views.group),
    path("reject", views.reject)

]
