# Default target
.PHONY: help run install lint format test clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the FastAPI app"
	@echo "  make lint       - Run linter (ruff or flake8)"
	@echo "  make format     - Format code (black)"
	@echo "  make test       - Run tests (if any)"
	@echo "  make clean      - Remove pycache and temporary files"

# Установка зависимостей
install:
	pip install -r requirements.txt

# Запуск приложения
run:
ifeq ($(OS),Windows_NT)
	powershell "$$env:PYTHONPATH='src'; uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
else
	PYTHONPATH=src uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
endif

# Линтер (опционально — можно добавить позже)
lint:
	ruff check src/

# Форматирование (опционально)
format:
	black src/

# Запуск тестов (если будут)
test:
	PYTHONPATH=src python -m pytest tests/

# Очистка
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true