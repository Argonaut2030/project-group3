from django.urls import path

from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.main, name='home'),
    path('<int:page>', views.main, name='root_paginate'),
    path('add_contact/', views.add_contact, name='add_contact'),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
    path('upcoming_birthdays/<int:days>/', views.upcoming_birthdays, name='upcoming_birthdays_with_days'),
    path('search_contacts/', views.search_contacts, name='search_contacts'),
    path('edit_contact/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
]