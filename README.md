# TexPark_Web

## Технопарк Mail.ru / 1й семестр / Web-технологии
- Техническое задание ([Markdown](https://github.com/ziontab/tp-tasks/blob/master/files/markdown/technical_details.md),<!-- [HTML](files/html/technical_details.html),--> [PDF](https://github.com/ziontab/tp-tasks/blob/master/files/pdf/technical_details.pdf))

# Installation

## Must be installed
- python3
- pip3
- virtualenv
- libmysqlclient-dev
- mysql-client
- libmemcached-dev

## Build python interpreter
- ./build

## Edit db.cnf
- nano db.cnf

## DB migrations
- ./venv/bin/python manage.py makemigrations SiteApp
- ./venv/bin/python manage.py migrate
