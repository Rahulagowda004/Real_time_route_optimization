FROM python:3.11-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN echo "TOMTOM_API_KEY=rGT85lmN9pMxHZFbcsYO3zFpGf2vcCKc\n\
OPENWEATHER_API_KEY=66c1b6b7e7ece7e19bdbc982d0f23530\n\
OPENCAGE_API_KEY=02040a72cde349c7a27d5aed2bd42e52\n\
FLASK_APP=app.py\n\
FLASK_ENV=development\n\
FLASK_DEBUG=1\n\
MYSQL_HOST=db\n\
MYSQL_USER=root\n\
MYSQL_PASSWORD=sudha010274\n\
MYSQL_DATABASE=translogi" > .env

EXPOSE 5000

CMD ["python", "app.py"]
