.PHONY: clean chat-api-service help

SHELL=/bin/bash

## Remove Python cache files
clean:
	find . -name "__pycache__" -type d -exec rm -r {} \+

## Run chat service locally
chat-api-service:
	poetry run uvicorn app.main:app --reload

## Display help information
help:
	@echo "Available commands:"
	@echo "  make clean         - Remove Python cache files"
	@echo "  make chat-api-service - Run chat service locally"
	@echo "  make help          - Display this help information"
# Default target
.DEFAULT_GOAL := help
