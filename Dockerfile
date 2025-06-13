FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories if they don't exist
RUN mkdir -p static

# Expose the port the app will run on
EXPOSE 8080

# Command to run the app
CMD ["python", "app.py"]
