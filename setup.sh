#!/bin/bash

# --------------------------------------------------------------------
# setup.sh - Initial Setup Script for Django + Docker Environment
# --------------------------------------------------------------------
# This script:
# 1. Creates a .env file if it doesn't exist by copying SAMPLE_ENV.txt
# 2. Makes entrypoint.sh executable
# 3. Builds and starts the Docker containers with docker-compose
# --------------------------------------------------------------------

set -e  # Exit immediately if a command exits with a non-zero status

# Step 1: Copy SAMPLE_ENV.txt to .env if .env doesn't exist
if [ ! -f ".env" ]; then
  echo "Creating .env file from SAMPLE_ENV.txt..."
  cp SAMPLE_ENV.txt .env
else
  echo ".env file already exists, skipping copy."
fi

# Step 2: Make entrypoint.sh executable
if [ -f "entrypoint.sh" ]; then
  echo "Making entrypoint.sh executable..."
  chmod +x entrypoint.sh
else
  echo "❌ entrypoint.sh not found! Make sure it exists in the project root."
  exit 1
fi

# Step 3: Build and run Docker containers
echo "Starting Docker containers with docker-compose..."
#docker-compose down --rmi local
#docker-compose down --volumes --remove-orphans
#docker system prune -f

docker-compose up --build