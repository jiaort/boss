#!/bin/bash

python3 manage.py migrate&&
uvicorn boss.asgi:application --host 0.0.0.0 --port 8000 --lifespan off
