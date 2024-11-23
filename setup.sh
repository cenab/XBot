#!/bin/bash

# Exit on errors
set -e

# Update and install necessary system packages
echo "Updating system packages..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv

# Create a Python virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Notify the user
echo "Setup complete. Activate the virtual environment with 'source venv/bin/activate'."
