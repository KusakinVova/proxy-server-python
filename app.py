import requests
from flask import Flask, request, Response
from bs4 import BeautifulSoup

app = Flask(__name__)

# Функция для получения содержимого страницы Hacker News

def get_hacker_news_page():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    return response.text

# Функция для модификации текста, добавляя "™" после слов из 6 букв
def modify_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all(text=True):
        words = tag.split()
        for i in range(len(words)):
            if len(words[i]) == 6:
                words[i] += '™'
        tag.replace_with(' '.join(words))
    return str(soup)


# Маршрут для обработки запросов
@app.route('/')
def hacker_news_proxy():
    hacker_news_page = get_hacker_news_page()
    modified_page = modify_text(hacker_news_page)
    return Response(modified_page, content_type='text/html; charset=utf-8')

if __name__ == '__main__':
    app.run(host='localhost', port=8232)