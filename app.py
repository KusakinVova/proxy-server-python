import requests
from flask import Flask, request, Response, redirect
from bs4 import BeautifulSoup

app = Flask(__name__)

# Функция для получения содержимого страницы Hacker News

def get_hacker_news_page(url):
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
    url = "https://news.ycombinator.com/"
    hacker_news_page = get_hacker_news_page(url)
    modified_page = modify_text(hacker_news_page)
    return Response(modified_page, content_type='text/html; charset=utf-8')

# Маршрут для обработки внутренних страниц
@app.route('/item')
def hacker_news_item():
    item_id = request.args.get('id')
    if item_id:
        url = f"https://news.ycombinator.com/item?id={item_id}"
        item_page = get_hacker_news_page(url)
        modified_page = modify_text(item_page)
        return Response(modified_page, content_type='text/html; charset=utf-8')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(host='localhost', port=8232)