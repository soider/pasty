.PHONY: dev
dev:
	python manage.py runserver 8000

install:
	python manage.py syncdb;
	python manage.py loaddata sources;
	pip install -r requirements.txt;

