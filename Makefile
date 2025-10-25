.PHONY: help install setup test run clean

help:
	@echo "AI News Bot - Available Commands"
	@echo "================================="
	@echo "  make install    - Install Python dependencies"
	@echo "  make setup      - Initial setup (copy .env.example, install deps)"
	@echo "  make test       - Run setup verification tests"
	@echo "  make run        - Run the news bot"
	@echo "  make examples   - Run usage examples"
	@echo "  make clean      - Clean up cache files"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Done!"

setup: install
	@echo "Setting up AI News Bot..."
	@if [ ! -f .env ]; then \
		echo "Creating .env from .env.example..."; \
		cp .env.example .env; \
		echo "Please edit .env with your actual credentials"; \
	else \
		echo ".env already exists, skipping..."; \
	fi
	@echo ""
	@echo "Setup complete! Next steps:"
	@echo "  1. Edit .env with your API keys"
	@echo "  2. Run 'make test' to verify setup"
	@echo "  3. Run 'make run' to generate news"

test:
	@echo "Running setup verification..."
	python test_setup.py

run:
	@echo "Running AI News Bot..."
	python main.py

examples:
	@echo "Running usage examples..."
	python example_usage.py

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	@echo "Done!"
