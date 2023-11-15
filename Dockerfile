# Use an official Python runtime as a parent image
FROM python:3.8.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /usr/src/app

# Install gcc and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Running as non-root user 
RUN useradd --create-home appuser
WORKDIR /home/appuser
COPY --chown=appuser:appuser . .
USER appuser

# Install dependencies
# Copy the requirements file into the container at /usr/src/app/
COPY requirements.txt /usr/src/app/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . /usr/src/app/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--worker-class", "gevent", "--workers", "3", "--bind", "0.0.0.0:8000", "message_api.wsgi:application"]
