#!/bin/bash
service mongod stop
mongod
python manage.py runserver
