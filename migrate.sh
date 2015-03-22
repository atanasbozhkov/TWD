#!/bin/bash

python manage.py makemigrations burger
python manage.py migrate
