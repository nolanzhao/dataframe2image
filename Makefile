.PHONY: help install test lint format build clean examples upload

help:
	@echo "Available commands:"
	@echo "  install    - Install package and dependencies"
	@echo "  test       - Run tests"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code"
	@echo "  build      - Build package"
	@echo "  clean      - Clean build artifacts"
	@echo "  examples   - Run examples"
	@echo "  upload     - Upload to PyPI (requires API token)"

install:
	pip install --upgrade pip
	pip install -e .
	playwright install chromium

test:
	python -m pytest tests/ -v

lint:
	flake8 src/ tests/ examples/
	mypy src/

format:
	black src/ tests/ examples/
	isort src/ tests/ examples/

build: clean
	pip install build twine
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f examples/*.png examples/*.jpg examples/*.jpeg examples/*.webp examples/*.html

examples:
	cd examples && python example_usage.py

upload: build
	python -m twine upload dist/*

dev-install: install
	pip install -e ".[dev]"
