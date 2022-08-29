#!/bin/bash
echo "Migrate"
python manage.py migrate

python manage.py wait_db

echo "Server"
python manage.py runserver 0.0.0.0:8000