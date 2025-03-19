from django.urls import path

from . import views


app_name = 'notes'


urlpatterns = [
    path('', views.main, name='notes_home'),
    path('page/<int:page>/', views.main, name='notes_paginate'),
    path('tag/', views.tag, name='add_tag'),
    path('add_note/', views.add_note, name='add_note'),
    path('search_notes/', views.search_notes, name='search_notes'),
    path('detail/<int:note_id>', views.detail_note, name='detail'),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
]