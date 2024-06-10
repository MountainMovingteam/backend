from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("query/answer", views.query_answer),
    path("query/problem", views.query_question),
    path("create/question", views.create_question),
    path("query/history", views.query_history)

]
