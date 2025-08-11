# Dockerfile
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt /tmp

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Copy the Flask app
COPY app.py app.py

COPY checklists/ checklists/

USER nobody

# Command to run the application
CMD ["python", "app.py"]

