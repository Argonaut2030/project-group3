# news/urls.py

from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('financial-news/', views.financial_news, name='financial_news'),
]
