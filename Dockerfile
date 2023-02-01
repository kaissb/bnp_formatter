# Use an official Python runtime as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Creating the directory where the files will be stored
RUN mkdir /d/bnp_format

# Run the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
