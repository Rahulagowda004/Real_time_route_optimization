# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install Node.js and pm2
RUN apt-get update && apt-get install -y nodejs npm && npm install -g pm2

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install npm dependencies
RUN npm install

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run both python app.py and npm run dev when the container launches
CMD ["pm2-runtime", "start", "app.py", "--interpreter", "python3", "--name", "app", "--", "&&", "npm", "run", "dev"]
