import requests
from flask import Flask, request, Response, redirect
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import re

app = Flask(__name__)

# Dictionary for page caching
page_cache = {}

# Function to get contents of Hacker News page with caching
def get_hacker_news_page(url):
    if url in page_cache:
        return page_cache[url]
    else:
        response = requests.get(url)
        page_content = response.text
        page_cache[url] = page_content
        return page_content

# Function for automatic cache clearing
def clear_cache():
    page_cache.clear()

# Initializing the task scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(clear_cache, 'interval', minutes=5)
scheduler.start()

# Register a function to stop the task scheduler 
# when the application ends
atexit.register(lambda: scheduler.shutdown())

# Function to modify text by adding "™" after 6 letter words
def modify_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all(text=True):
        words = tag.split(' ')
        for i in range(len(words)):
            if len(words[i]) == 6:
                words[i] += '™'
        tag.replace_with(' '.join(words))
    return str(soup)

# Function for changing resource links
def modify_resources(text, base_url):
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all(['link', 'script', 'img'], src=True):
        if not tag['src'].startswith(('http://', 'https://')):
            tag['src'] = f"{base_url}{tag['src']}"
    return str(soup)

# Route for processing requests to the root page
@app.route('/')
def hacker_news_proxy():
    url = "https://news.ycombinator.com/"
    hacker_news_page = get_hacker_news_page(url)
    modified_page = modify_text(hacker_news_page)

    modified_page_with_resources = modify_resources(modified_page, url)
    return Response(modified_page_with_resources, content_type='text/html; charset=utf-8')

# Route for processing internal pages
@app.route('/<page_type>')
def hacker_news_page(page_type):

    params = request.args.to_dict()
    if page_type and params:
        getparams = ''
        for key, value in params.items():
            getparams += f"{key}={value}&"
        url = f"https://news.ycombinator.com/{page_type}?{getparams}"
    elif page_type:
        url = f"https://news.ycombinator.com/{page_type}"
    else:
        return redirect('/')
    
    page_content = get_hacker_news_page(url)
   
    pattern = r'https://[^\s]+(?:\.css|\.js)[^\s]*'
    matches = re.findall(pattern, url)
    if not matches:
        page_content = modify_text(page_content)
    
    base_url = "https://news.ycombinator.com/"
    modified_page_with_resources = modify_resources(page_content, base_url)
    return Response(modified_page_with_resources, content_type='text/html; charset=utf-8')

if __name__ == '__main__':
    app.run(host='localhost', port=8232)