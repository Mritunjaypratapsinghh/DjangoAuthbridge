FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev
# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY .env /app/.env

# Copy the rest of the Django project files into the container
COPY . /app

# Expose the Django development server port
EXPOSE 8000

# Default command to run the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
