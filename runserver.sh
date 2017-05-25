#/bin/bash
# The command above states wich shell is used
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

echo "----- Activating virtual enviroment -----"
source venv/bin/activate

echo "----- Running the server -----"
python manage.py runserver

echo "----- Deactivating Virtual Enviroment -----"
deactivate