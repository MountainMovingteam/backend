from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login),
    path("register", views.register),
    path("getInfo", views.get_info),
    path("modify/password", views.modify_password),
    path("notice", views.notice),
    path("notice/info", views.notice_info),
    path("pictures", views.pictures),
    path("push", views.push),
    path("editInfo", views.edit_info)
]
