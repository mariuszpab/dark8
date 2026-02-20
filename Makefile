# Makefile for DARK8 OS

.PHONY: help install dev test lint format clean run api docs

PYTHON := python3
PIP := $(PYTHON) -m pip
PROJECT := dark8_core

help:
	@echo "🖤 DARK8 OS - Makefile"
	@echo ""
	@echo "Available targets:"
	@echo "  make install      - Install dependencies"
	@echo "  make dev          - Install development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Check code style (pylint, mypy)"
	@echo "  make format       - Format code (black, isort)"
	@echo "  make clean        - Clean up cache and artifacts"
	@echo "  make run          - Run DARK8 CLI"
	@echo "  make api          - Run DARK8 API server"
	@echo "  make docs         - Build documentation"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -r requirements.txt
	@echo "✓ Installation complete"

dev: install
	$(PIP) install -r requirements-dev.txt
	pre-commit install
	@echo "✓ Development setup complete"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=$(PROJECT) --cov-report=html --cov-report=term
	@echo "Coverage report: htmlcov/index.html"

lint:
	@echo "Checking with pylint..."
	pylint $(PROJECT)/ --exit-zero || true
	@echo "Checking with mypy..."
	mypy $(PROJECT)/ --ignore-missing-imports || true
	@echo "✓ Lint checks complete"

format:
	@echo "Formatting with black..."
	black $(PROJECT)/ tests/
	@echo "Sorting imports with isort..."
	isort $(PROJECT)/ tests/
	@echo "✓ Code formatted"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build
	@echo "✓ Cleanup complete"

run:
	$(PYTHON) -m $(PROJECT)

api:
	$(PYTHON) -m $(PROJECT) --mode api

docs:
	@echo "Documentation generation (TODO)"
	@echo "See: docs/"

docker-build:
	docker build -t dark8-os:latest .

docker-run:
	docker run -it -p 8000:8000 dark8-os:latest

docker-dev:
	docker run -it -p 8000:8000 \
		-v $(PWD):/app \
		-e DARK8_DEBUG=true \
		dark8-os:latest

security:
	@echo "Running security checks..."
	bandit -r $(PROJECT)/ -ll || true
	@echo "✓ Security checks complete"

setup-linux:
	./scripts/setup_env.sh

setup-windows:
	scripts\setup_env.bat

requirements-check:
	pip-audit || true
	@echo "✓ Requirements check complete"

.DEFAULT_GOAL := help
