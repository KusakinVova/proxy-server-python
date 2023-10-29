# Hacker™ News proxy

Простой http-прокси-сервер, запускаемый локально, который показывает содержимое страниц [Hacker News](https://news.ycombinator.com).

## Задача

Условия:

[x] Python™ 3.9+

[x] страницы должны™ отображаться и работать полностью корректно, в точности так, как и оригинальные (за исключением модифицированного текста™);

[x] при навигации по ссылкам, которые ведут на другие™ страницы HN, браузер должен™ оставаться на адресе™ вашего™ прокси™;

[x] можно использовать любые общедоступные библиотеки, которые сочтёте нужным™;

[x] чем меньше™ кода, тем лучше. PEP8 — обязательно;

[x] если в условиях вам не хватает каких-то данных™, опирайтесь на здравый смысл.

Прокси модицифировать текст на страницах, после каждого слова из шести букв ставит:

Исходный текст: https://news.ycombinator.com/item?id=13713480

```
The visual description of the colliding files, at
http://shattered.io/static/pdf_format.png, is not very helpful
in understanding how they produced the PDFs, so I took apart
the PDFs and worked it out.

Basically, each PDF contains a single large (421,385-byte) JPG
image, followed by a few PDF commands to display the JPG. The
collision lives entirely in the JPG data - the PDF format is
merely incidental here. Extracting out the two images shows two
JPG files with different contents (but different SHA-1 hashes
since the necessary prefix is missing). Each PDF consists of a
common prefix (which contains the PDF header, JPG stream
descriptor and some JPG headers), and a common suffix (containing
image data and PDF display commands).
```

Результат прокси™: http://127.0.0.1:8232/item?id=13713480

```
The visual™ description of the colliding files, at
http://shattered.io/static/pdf_format.png, is not very helpful
in understanding how they produced the PDFs, so I took apart
the PDFs and worked™ it out.

Basically, each PDF contains a single™ large (421,385-byte) JPG
image, followed by a few PDF commands to display the JPG. The
collision lives entirely in the JPG data - the PDF format™ is
merely™ incidental here. Extracting out the two images™ shows two
JPG files with different contents (but different SHA-1 hashes™
since the necessary prefix™ is missing). Each PDF consists of a
common™ prefix™ (which contains the PDF header™, JPG stream™
descriptor and some JPG headers), and a common™ suffix™ (containing
image data and PDF display commands).
```

## Результат

Код представляет собой Flask-приложение, которое работает как прокси-сервер для Hacker News и выполняет несколько действий:

1. Он создает кэш для сохранения полученных страниц Hacker News, чтобы уменьшить количество запросов к исходному серверу.
2. Периодически (каждые 5 минут) очищает кэш для обновления данных.
3. Модифицирует текст на страницах Hacker News, добавляя символ "™" после каждого слова, состоящего из 6 букв.
4. Изменяет ссылки на ресурсы (стили, скрипты, изображения), чтобы они указывали на адрес вашего прокси-сервера вместо исходных адресов.

Здесь есть несколько маршрутов:

- Маршрут '/' отвечает за корневую страницу и получает содержимое Hacker News, модифицирует его с помощью modify_text, и затем изменяет ресурсы на этой странице с помощью modify_resources.

- Маршрут '/<page_type>' отвечает за другие внутренние страницы Hacker News (например, /new, /ask, /show), а также обрабатывает параметры запроса (query parameters) и модифицирует содержимое страницы.

Если вам нужно использовать этот код, убедитесь, что у вас установлены все необходимые библиотеки (Flask, requests, beautifulsoup4, apscheduler), и вы можете запустить приложение, посетив http://localhost:8232 в вашем веб-браузере. Вы также можете обращаться к различным внутренним страницам Hacker News, добавляя их к базовому URL (например, http://localhost:8232/new).
