from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("query/answer", views.query_ans),
    path("search", views.query_vague),
    path('create/problem', views.create_problem)
]
