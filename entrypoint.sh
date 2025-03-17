#!/bin/sh

# Execute migrations
python manage.py migrate
# Configure the default groups for this app
python manage.py creategroups
# Run server
python manage.py runserver 0.0.0.0:8000
