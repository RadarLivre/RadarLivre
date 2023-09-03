#!/bin/bash
# The command above states wich shell is used
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

echo "----- Activating virtual enviroment -----"
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo "----- Virtual environment activated successfully -----"
else
    echo "************************************************************"
    echo "| Error: Failed to activate virtual environment            |"
    echo "| Installation aborted                                     |"
    echo "************************************************************"
    exit 1  # Saia do script 
fi

echo "----- Running the server -----"
python3 manage.py runserver

echo "----- Deactivating Virtual Enviroment -----"
deactivate
