import requests
from bs4 import BeautifulSoup
import re

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'

try:
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    found_count = 0

    for article in soup.find_all('article'):
        title_tag = article.find('h2')
        if not title_tag:
            continue

        title_link = title_tag.find('a')
        if not title_link:
            continue

        title = title_link.text.strip()
        href = title_link.get('href', '')
        link = 'https://habr.com' + href if href.startswith('/') else href

        time_tag = article.find('time')
        date = time_tag.get('title', 'Нет даты').split(',')[0] if time_tag else 'Нет даты'

        search_text = title.lower()
        content = article.find('div', class_=lambda x: x and ('article-formatted-body' in x or 'tm-article-body' in x))
        if content:
            search_text += ' ' + content.text.strip().lower()

        found = any(re.search(r'\b' + re.escape(k.lower()) + r'\b', search_text) for k in KEYWORDS)

        if found:
            print(f'{date} – {title} – {link}')
            found_count += 1

except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к сайту: {e}")
    print("Проверьте подключение к интернету, корректность ссылки  и попробуйте снова.")