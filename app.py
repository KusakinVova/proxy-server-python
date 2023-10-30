import requests
from flask import Flask, request, Response, redirect
from bs4 import BeautifulSoup
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import re

URL_SOURCE = "https://news.ycombinator.com"

app = Flask(__name__)

# Dictionary for page caching
page_cache = {}

# Function to get contents of Hacker News page with caching
def get_page(url):
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
            # using a regular to check that a word of 6 letters
            if re.match(r'^[a-zA-Z]{6}$', words[i]):
                words[i] += '™'
        tag.replace_with(' '.join(words))
    return str(soup)


def modify_css(css_text, base_url):
    regex_pattern = r'url\("([^"]+)"\)'
    replacement = r'url("{}/\1")'.format(base_url)
    modified_css_text = re.sub(regex_pattern, replacement, css_text)
    return modified_css_text


# Function for changing resource links
def modify_resources(text, base_url):
    soup = BeautifulSoup(text, 'html.parser')
    for tag in soup.find_all(['link', 'script', 'img'], src=True):
        if not tag['src'].startswith(('http://', 'https://')):
            tag['src'] = f"{base_url}/{tag['src']}"
    for tag in soup.find_all(['a', 'link'], href=True):
        if tag['href'] == base_url:
            tag['href'] = '/'
        if tag['href'] == "favicon.ico":
            tag['href'] = f"{base_url}/{tag['href']}"
    return str(soup)

# Route for processing requests to the root page
@app.route('/')
def route_page_main():
    page_content = get_page(URL_SOURCE)
    modified_page = modify_text(page_content)

    modified_page_with_resources = modify_resources(modified_page, URL_SOURCE)
    return Response(modified_page_with_resources, content_type='text/html; charset=utf-8')

# Route for processing internal pages
@app.route('/<page_type>')
def route_page_other(page_type):

    params = request.args.to_dict()
    if page_type and params:
        getparams = ''
        for key, value in params.items():
            getparams += f"{key}={value}&"
        url = f"{URL_SOURCE}/{page_type}?{getparams}"
    elif page_type:
        url = f"{URL_SOURCE}/{page_type}"
    else:
        return redirect('/')
    
    page_content = get_page(url)
   
    pattern = r'https://[^\s]+(?:\.css|\.js)[^\s]*'
    matches = re.findall(pattern, url)
    if not matches:
        page_content = modify_text(page_content)
    if 'news.css' in url:
        page_content = modify_css(page_content, URL_SOURCE)
    
    modified_page_with_resources = modify_resources(page_content, URL_SOURCE)
    return Response(modified_page_with_resources, content_type='text/html; charset=utf-8')

if __name__ == '__main__':
    app.run(host='localhost', port=8232)