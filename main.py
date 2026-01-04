import requests
from bs4 import BeautifulSoup

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
        if time_tag:
            date = time_tag.get('datetime', '').split('T')[0] \
                if time_tag.get('datetime') else time_tag.text.strip()
        else:
            date = 'Без даты'

        search_text = title.lower()
        preview_div = article.find('div', class_='tm-article-body tm-article-snippet__lead')
        if preview_div and preview_div.text:
            search_text += ' ' + preview_div.text.strip().lower()

        if any(word in search_text for word in KEYWORDS):
            print(f'{date} – {title} – {link}')
            found_count += 1

except requests.exceptions.RequestException as e:
    print(f"Ошибка при запросе к сайту: {e}")
    print("Проверьте подключение к интернету, корректность ссылки и попробуйте снова.")