FROM python:3.11

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Copy the service account key
COPY service-account-key.json /app/service-account-key.json

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "src/main.py"]