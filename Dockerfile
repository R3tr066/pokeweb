FROM python:3.12.11-alpine3.22

# Install system dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip setuptools wheel

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000

# Use the correct WSGI path
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "pokeweb.wsgi:application"]
