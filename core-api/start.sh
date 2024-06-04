#!/bin/bash

exec gunicorn --bind :8000 --workers 1 --threads 8 --timeout 0 wsgi:g_app