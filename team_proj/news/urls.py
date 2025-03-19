# urls.py
from django.urls import path
from . import views

app_name = 'news'  # Це має бути вказано, щоб мати можливість використовувати простір імен

urlpatterns = [
    path('financial-news/', views.financial_news, name='financial_news'),
    # інші маршрути
]
