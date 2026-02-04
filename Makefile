mig:
	uv run python3 manage.py makemigrations
	uv run python3 manage.py migrate

run:
	uv run python3 manage.py runserver
