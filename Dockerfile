# Use an official Python image from DockerHub
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy your code into the container
COPY . .

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt || echo "No requirements file"

# Run a test command
CMD ["echo", "Docker container is working!"]
