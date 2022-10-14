release: python manage.py makemigrations
release: python manage.py migrate
web: gunicorn gradebook_project.wsgi --log-file -