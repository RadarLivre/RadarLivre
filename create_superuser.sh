#/bin/bash
# The command above states wich shell is used

# This file is used to set up the project installing all requirements and dependencies
# Keep it as automated as possible, as the software must be easy enough for everyone to install
# Use ----- <Description> ----- to help users track installation proccess and possible errors.

# Every step is divided in sections as the following, so it is easier to track error and program

echo "************************************************************"
echo "| This is going to help you create a new superuser, so you |"
echo "| have administrator privileges for accessing the server.  |"
echo "| for you.                                                 |"
echo "| This may take several minutes. Please, be patient.       |"
echo "************************************************************"

echo "----- Activating virtual enviroment -----"
source venv/bin/activate

echo "----- Creating new superuser -----"
echo "You will be asked to provide a username, email and password. For security reasons, your password need to be strong."
python manage.py createsuperuser

echo "----- Activating virtual enviroment -----"
source deactivate
