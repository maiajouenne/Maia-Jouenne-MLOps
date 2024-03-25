prepare:
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	poetry run streamlit run app.py

check:
	poetry run vulture .
	poetry run isort .
	poetry run black .

build:
	docker build -t maia-jouenne-mlops-app:v1 .

push:
	docker push maia-jouenne-mlops-app:v1
