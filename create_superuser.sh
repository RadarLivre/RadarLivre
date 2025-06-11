#!/bin/bash
# The command above states wich shell is used
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Activating virtual enviroment..."
    source .venv/bin/activate
fi

echo "Creating superuser..."
python manage.py createsuperuser

echo "Deactivating Virtual Enviroment..."
deactivate