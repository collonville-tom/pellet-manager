#!/bin/sh

python manage.py makemigrations pellet_mgmt_app
python manage.py migrate
python manage.py runserver 0.0.0.0:8000