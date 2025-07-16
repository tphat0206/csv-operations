FROM python:3.11-slim

WORKDIR /app


RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

 CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]