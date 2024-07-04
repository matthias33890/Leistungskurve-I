# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make entrypoint.sh executable
RUN chmod +x /app/entrypoint.sh
RUN chmod +x init.sh

# Expose port 8501 for streamlit
EXPOSE 8501

# Run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
