# Use a Python image with ffmpeg pre-installed
FROM jrottenberg/ffmpeg:4.4-ubuntu

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set the working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# List files to confirm the working directory
RUN ls -la /app

# Set the default command
CMD ["python3", "bot.py"]
