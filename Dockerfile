FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/emails /app/instance && \
    chmod -R 755 /app/emails /app/instance

# Expose ports
EXPOSE 5000 1025

# Run the application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
