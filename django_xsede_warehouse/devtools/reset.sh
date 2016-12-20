#!/bin/bash -x
rm -i -v */migrations/00*
manage.py makemigrations
manage.py migrate
manage.py createsuperuser --username admin --email jpfnavarro@gmail.com
manage.py migrate --database=glue2
