#!/bin/bash

chown www-data:www-data /var/www/college_despamifier/db.sqlite3

python3 /var/www/college_despamifier/manage.py makemigrations

python3 /var/www/college_despamifier/manage.py migrate --database=default

service nginx start

uwsgi --ini /var/www/college_despamifier/uwsgi.ini