

# Create your views here.
# news/views.py

from django.shortcuts import render
import requests

# Функція для отримання фінансових новин з Alpha Vantage
def get_financial_news():
    url = "https://www.alphavantage.co/query"
    params = {
        'function': 'NEWS_SENTIMENT',
        'symbol': 'MSFT',
        'apikey': 'RKH85LHYW46A30RI',
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Перевірка на успішний статус запиту
        data = response.json()

        # Перевірка на наявність новин у відповіді
        if 'feed' in data:
            feed = data['feed']
            formatted_articles = []
            for article in feed:
                formatted_articles.append({
                    'title': article.get('title'),
                    'summary': article.get('summary'),
                    'url': article.get('url'),
                    'time_published': article.get('time_published'),
                    'source': article.get('source'),
                    'banner_image': article.get('banner_image'),
                })
            return formatted_articles
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
