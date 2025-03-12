#!/bin/sh

# Execute migrations
./manage.py migrate
# Configure the default groups for this app
./manage.py creategroups
# Generate the openapi schema
./manage.py spectacular --color --file schema.yml
# Run server
./manage.py runserver 0.0.0.0:8000
