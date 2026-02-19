# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required for OpenCV, Tkinter, App, and Audio
RUN apt-get update && apt-get install -y \
    python3-tk \
    libgl1-mesa-glx \
    libgtk-3-0 \
    espeak \
    libespeak-dev \
    libasound2-dev \
    portaudio19-dev \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Create a non-root user (optional but recommended, though for GUI/HW access sometimes root is easier in dev)
# For simplicity in this demo ensuring HW access, we run as root or default.

# Command to run the application
CMD ["python", "VigilantiAI.py"]
