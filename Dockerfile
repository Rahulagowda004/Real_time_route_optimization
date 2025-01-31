FROM python:3.11-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN echo "TOMTOM_API_KEY=None\n\
OPENWEATHER_API_KEY=None\n\
OPENCAGE_API_KEY=None\n\
FLASK_APP=app.py\n\
FLASK_ENV=development\n\
FLASK_DEBUG=1\n\
MYSQL_HOST=db\n\
MYSQL_USER=root\n\
MYSQL_PASSWORD=None\n\
MYSQL_DATABASE=translogi" > .env

EXPOSE 5000

CMD ["python", "app.py"]
