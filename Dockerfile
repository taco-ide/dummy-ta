# Notes:
# 1. If GPU usage is required in future Docker configurations (e.g., with NVIDIA), modify this Dockerfile with GPU-enabled libraries and drivers.

# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    python3-pip \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy application files
COPY . .

# Add application to PYTHONPATH
ENV PYTHONPATH="/app"

# Expose API port
EXPOSE 8899

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8899"]

