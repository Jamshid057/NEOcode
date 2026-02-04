mig:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

run:
	gunicorn root.wsgi:application
