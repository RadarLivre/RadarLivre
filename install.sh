#!/bin/bash

# Enter relative directory
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

echo "Starting RadarLivre Server installation..."

echo "Configuring virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing Python requirements..."
pip install -r requirements.txt

echo "Configuring database..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Collecting static files..."
python3 manage.py collectstatic --no-input

deactivate

echo "Installation completed!"
echo "To start the server, execute: ./runserver.sh"