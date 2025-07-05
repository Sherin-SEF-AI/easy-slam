#!/bin/bash

# Development installation script for easy-slam

echo "Installing easy-slam in development mode..."

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest sphinx jupyter black flake8

# Install package in development mode
pip install -e .

echo "Installation complete!"
echo "To activate the virtual environment: source venv/bin/activate"
echo "To run tests: python -m pytest tests/"
echo "To build docs: cd docs && make html" 