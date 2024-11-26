#!/bin/bash

python3 manage.py migrate&&
gunicorn boss.wsgi -c gunicorn.py
