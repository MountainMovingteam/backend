from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login),
    path("register", views.register),
    path("getInfo", views.get_info),
    path("getAvatar", views.get_avatar),
    path("modify/password", views.modify_password),
    path("notice", views.notice),
    path("notice/info", views.notice_info),
    path("read", views.notice_read),
    path("notice/delete", views.notice_delete),
    path("pictures", views.pictures),
    path("push", views.push),
    path("editInfo", views.edit_info),
    path("addPicture", views.add_picture),
    path("addPush", views.add_push),
    path("orderLog", views.get_order_log),
    path("getPublicKey", views.get_public_key),
    path("register/sendMessage", views.send_message),
    path("passwordEncode", views.password_encode)
]
