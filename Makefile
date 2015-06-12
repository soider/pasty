.PHONY: dev
dev:
	python manage.py runserver 8000

shell:
	python manage.py shell

install:
	python manage.py syncdb;
	python manage.py loaddata sources;
	pip install -r requirements.txt;

celery:
	celery -A pasty worker  --loglevel=debug

beat:
	celery -A pasty beat --loglevel=debug