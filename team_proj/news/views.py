from django.shortcuts import render
import requests
from datetime import datetime

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
            for article in feed[:10]:  # Обрізаємо до перших 10 новин
                # Форматування дати
                try:
                    time_published = article.get('time_published')
                    if time_published:
                        # Перетворення дати з формату "yyyyMMdd'T'HHmmss"
                        formatted_date = datetime.strptime(time_published, "%Y%m%dT%H%M%S").strftime("%B %d, %Y, %I:%M %p")
                    else:
                        formatted_date = "Дата не вказана"
                except Exception as e:
                    formatted_date = "Помилка при форматуванні дати"
                    print(f"Error formatting date: {e}")

                formatted_articles.append({
                    'title': article.get('title'),
                    'summary': article.get('summary'),
                    'url': article.get('url'),
                    'time_published': formatted_date,  # Додаємо відформатовану дату
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
