python manage.py migrate

python manage.py collectstatic --clear --noinput

gunicorn short_tracker.wsgi:application --bind 0.0.0.0:8000