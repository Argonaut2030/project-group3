from django.urls import path

from . import views

app_name = 'file_manager'

urlpatterns = [
    path('', views.list_files, name='file_list'),
    path('file-upload', views.upload_file, name='file_upload'),
]