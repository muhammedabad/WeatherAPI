#!/bin/bash

# Run migrations, if any.
python manage.py migrate

# Start django development server
python manage.py runserver 0.0.0.0:8000
