from django.urls import path

from . import views



app_name = 'notes'


urlpatterns = [
    path('', views.main, name='home'),
    path('page/<int:page>/', views.main, name='root_paginate'),  # Add 'page/' prefix
    path('tag/', views.tag, name='tag'),
    path('add/', views.add_note, name='add_note'),
    path('search_notes/', views.search_notes, name='search_notes'),
    # path('detail/<int:note_id>', views.detail, name='detail'),
    # path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    # path('delete_note/<int:note_id>/', views.delete_note, name='delete_contact'),
]

