# Use official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything else (including .py files and folders like data/)
COPY . .

# Create output folder (if not created by app)
RUN mkdir -p output

# Run your main script
CMD ["python", "main.py"]
