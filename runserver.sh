#!/bin/sh
# The command above states wich shell is used
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

echo "Activating virtual enviroment..."
source .venv/bin/activate

echo "Running the server..."
python3 manage.py runserver 0.0.0.0:8000

echo "Deactivating virtual enviroment..."
deactivate

# gunicorn --config gunicorn.conf.py radarlivre.wsgi:application