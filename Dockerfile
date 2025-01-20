# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install Python dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Install required system dependencies
RUN apt-get update && apt-get install -y wget unzip && \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean 

# Expose the port your Flask app will run on
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]