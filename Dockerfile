# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn python-dotenv google-generativeai

# Expose port
EXPOSE 8080

# Run app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]