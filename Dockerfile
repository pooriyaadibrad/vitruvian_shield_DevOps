# Use the official slim Python 3.11 image from the Docker Hub  
FROM python:3.11-slim  

# Set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from creating .pyc files  
ENV PYTHONUNBUFFERED 1          # Flush stdout and stderr immediately  

# Set the working directory in the container  
WORKDIR /app  

# Install system dependencies  
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*  

# Copy the requirements file into the container  
COPY requirements.txt /app/  

# Install Python dependencies  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of your application code into the container  
COPY . /app/  
