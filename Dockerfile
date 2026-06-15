FROM python:3.11-slim

# Install system dependencies (Tesseract, Poppler, etc.)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire application
COPY . .

# Create directories for uploads and reports
RUN mkdir -p uploads reports

# Expose port 8000
EXPOSE 8000

# Run the app
CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]