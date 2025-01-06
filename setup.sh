#!/bin/bash

# Update package list and install ffmpeg
apt-get update && apt-get install -y ffmpeg

# Run the Python script
python3 bot.py
