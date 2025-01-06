# Start with a Python base image that has ffmpeg pre-installed
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Confirm bot.py exists
RUN ls -la /app

# Set the default command to run your bot
CMD ["python3", "bot.py"]
