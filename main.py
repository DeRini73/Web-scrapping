import requests
from bs4 import BeautifulSoup

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
URL = 'https://habr.com/ru/articles/'

html = requests.get(URL).text
soup = BeautifulSoup(html, 'html.parser')

output_file = 'Результаты поиска.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    for article in soup.find_all('article'):
        title_tag = article.find('h2').find('a')
        if not title_tag:
            continue

        title = title_tag.text
        link = title_tag.get('href', '')
        time_tag = article.find('time')
        date = time_tag.get('title', 'Нет даты').split(',')[0] if time_tag else 'Нет даты'
        text = title.lower()
        content = article.find('div', class_=lambda x: x and ('article-formatted-body' in x or 'tm-article-body' in x))

        if content:
            text += ' ' + content.text.lower()

        if any(word in text for word in KEYWORDS):
            line = f'{date} – {title} – {link}'
            print(line)
            file.write(line + '\n')

print(f'Готово! Результаты поиска сохранены в {output_file}')