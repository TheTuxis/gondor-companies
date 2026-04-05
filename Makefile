.PHONY: run test lint format docker

run:
	uvicorn app.main:app --reload --port 8019

test:
	pytest -v

lint:
	ruff check .
	ruff format --check .

format:
	ruff format .

docker:
	docker build -t gondor-companies .
