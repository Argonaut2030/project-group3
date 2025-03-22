from django.urls import path

from . import views

app_name = 'file_manager'

urlpatterns = [
    path('', views.list_files, name='file_list'),
    path('file-upload', views.upload_file, name='file_upload'),
    path("file-search", views.search_files, name="search_files"),
    path("file-delete/<int:file_id>", views.delete_file, name="delete_file"),
    path('<int:page>', views.list_files, name='files_paginate'),
]