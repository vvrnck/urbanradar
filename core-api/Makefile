SHELL=/bin/bash

migrate:
	flask db upgrade head

fixture:
	python fixtures.py

start:
	gunicorn --bind :8000 --workers 1 --threads 8 --timeout 0 wsgi:g_app

.PHONY: migrate fixture start