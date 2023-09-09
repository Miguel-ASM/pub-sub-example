# Use the official Python image from Docker Hub as the base image
FROM python:3.9.18

# Set environment variables to prevent buffering of Python output and ensure Python output is sent straight to terminal without being buffered
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Pipenv
RUN pip install pipenv

# Create and set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the container
COPY Pipfile Pipfile.lock /app/

# Install project dependencies using Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port your application will run on (if applicable)
# EXPOSE 8000

# Command to run the application (replace with your actual command)
# CMD ["pipenv", "run", "python", "your_app.py"]