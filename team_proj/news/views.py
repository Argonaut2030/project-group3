# Create your views here.
# news/views.py

from django.shortcuts import render
import requests

# Функція для отримання фінансових новин з Alpha Vantage
def get_financial_news():
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'NEWS_SENTIMENT',
        'symbol': 'MSFT',  # Можна змінити на бажану валюту чи акцію
        'apikey': 'RKH85LHYW46A30RI',  # Ваш API ключ
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Перевірка на успішний статус запиту
        data = response.json()

        if 'articles' in data:
            return data['articles']
        else:
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

# Вигляд для відображення новин
def financial_news(request):
    news = get_financial_news()  # Отримуємо новини за допомогою функції
    if not news:
        message = "Не вдалося отримати новини."
    else:
        message = ""

    context = {
        'news': news,
        'message': message,
    }
    return render(request, 'news/financial_news.html', context)
