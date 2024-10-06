run:
	python manage.py runserver

make:
	python manage.py makemigrations
	python manage.py migrate

createuser:
	python manage.py createsuperuser

