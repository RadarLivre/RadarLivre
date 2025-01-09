#!/bin/sh
# The command above states wich shell is used
#BASEDIR=$(dirname "$0")
#cd "$BASEDIR"
#
#echo "----- Activating virtual enviroment -----"
#source venv/bin/activate
#
#echo "----- Running the server -----"
#python3 manage.py runserver
#
#echo "----- Deactivating Virtual Enviroment -----"
#deactivate

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0.0.0.0:8000