# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /joblisting-api-django

# Copy the requirements file into the container at /app
COPY requirements.txt /joblisting-api-django/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /joblisting-api-django/

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable for Django settings
ENV DJANGO_SETTINGS_MODULE=core.settings

# Run Django's development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]