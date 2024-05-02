from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("search", views.query_place),
    path("search/details", views.query_order),
    path("search/details/group", views.query_team_order),
    path("reject", views.reject_application),
    path("lecturer", views.query_all_lecturer),
    path("lecturer/find", views.query_lecturer),
    path("lecturer/edit", views.modify_lecture_info),
    path("lecturer/add", views.add_lecturer),
    path("lecturer/delete", views.delete_lecturer),
    path("lecturerAll", views.delete_all_lecturer),
]
