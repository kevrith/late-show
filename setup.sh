#!/bin/bash

echo "=== Late Show API Setup Script ==="
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if database exists
if [ ! -f "instance/app.db" ]; then
    echo "Setting up database..."
    flask db upgrade
    echo "Seeding database..."
    python seed.py
else
    echo "Database already exists. Skipping migration and seed."
    echo "To reset the database, delete instance/app.db and run this script again."
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "The API will be available at http://localhost:5555"
echo ""
