mig:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

run:
	gunicorn root.wsgi:application --bind 0.0.0.0:$PORT --workers 2
