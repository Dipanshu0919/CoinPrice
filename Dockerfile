# Start with a lightweight Python image
FROM python:3.9-slim

# Install system dependencies, including ffmpeg and necessary tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    curl \
    git \
    gpp \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure ffmpeg is functional
RUN ffmpeg -version

# Ensure yt_dlp recognizes ffmpeg
RUN python3 -m yt_dlp --version

# Set the default command to run your bot
CMD ["python3", "bot.py"]
