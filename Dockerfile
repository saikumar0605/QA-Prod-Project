# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpoppler-cpp-dev pkg-config python3-dev && \
    apt-get clean

# Set work directory
WORKDIR /app

# Copy requirements (create requirements.txt if not present)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Start server (update to your Django app's wsgi module if needed)
CMD ["gunicorn", "rag-prod.wsgi:application", "--bind", "0.0.0.0:8000"]
