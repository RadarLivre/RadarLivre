#!/bin/bash
# The command above states wich shell is used

# This file is used to set up the project installing all requirements and dependencies
# Keep it as automated as possible, as the software must be easy enough for everyone to install
# Use ----- <Description> ----- to help users track installation proccess and possible errors.

# Every step is divided in sections as the following, so it is easier to track error and program

# Enter relative directory
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

echo "************************************************************"
echo "| This is going to help you create a new superuser, so you |"
echo "| have administrator privileges for accessing the server.  |"
echo "| for you.                                                 |"
echo "| This may take several minutes. Please, be patient.       |"
echo "************************************************************"

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

echo "----- Creating new superuser -----"
echo "You will be asked to provide a username, email and password. For security reasons, your password need to be strong."
python3 manage.py createsuperuser

echo "----- Deactivating virtual enviroment -----"
deactivate
