# Use the official Python base image
FROM python:3.10

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the project's pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the project files to the container
COPY . /app/

# Expose the port your Django app will run on
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
