python manage.py migrate

python manage.py collectstatic --clear --noinput

gunicorn meeco.wsgi:application --bind 0.0.0.0:8000