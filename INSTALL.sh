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
echo "| The installation of the RadarLivre Server has just begun.|"
echo "| The system is going to install and configure everything  |"
echo "| for you.                                                 |"
echo "| This may take several minutes. Please, be patient.       |"
echo "************************************************************"

echo "************************************************************"
echo "| Updating apt-get                                         |"
echo "************************************************************"

sudo apt-get update -y
sudo apt-get upgrade -y

echo "************************************************************"
echo "| Started Installing Software Requirements                 |"
echo "************************************************************"

echo "----- Installing Virtualenv -----"
sudo apt-get install python3-virtualenv

echo "----- Installing SQLite -----"
sudo apt-get install sqlite3 libsqlite3-dev

echo "************************************************************"
echo "| Creating Virtual Enviroment                              |"
echo "************************************************************"

virtualenv venv

echo "************************************************************"
echo "| Configuring Virtual Enviroment                           |"
echo "************************************************************"

echo "----- Activating virtual enviroment -----"
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo "************************************************************"
    echo "| Virtual environment activated successfully               |"
    echo "************************************************************"

echo "----- Virtual environment activated -----"

else
    echo "************************************************************"
    echo "| Error: Failed to activate virtual environment            |"
    echo "| Installation aborted                                     |"
    echo "************************************************************"
    exit 1  # Saia do script 
fi

# The next steps will be executed while the virtual enviroment is activated.
# As Django comes with Pip installed, there is no need to install it.

echo "************************************************************"
echo "| Installing Virtual Enviroment Requirements               |"
echo "************************************************************"

echo "----- Installing Appdirs -----"
pip install appdirs==1.4.4

echo "----- Installing Django -----"
pip install Django==4.2.4

echo "----- Installing Django Appconfig -----"
pip install django-appconf==1.0.5

echo "----- Installing Django Cleanup -----"
pip install django-cleanup==8.0.0

echo "----- Installing Django Crispy Forms -----"
pip install django-crispy-forms==2.0

echo "----- Installing Django Filter -----"
pip install django-filter==23.2

echo "----- Installing Django Imagekit -----"
pip install django-imagekit==4.1.0

echo "----- Installing Django Rest -----"
pip install django-rest==0.8.7

echo "----- Installing Django Rest Framework -----"
pip install djangorestframework==3.14.0

echo "----- Installing Django Rest Framework Jsonp -----"
pip install djangorestframework-jsonp==1.0.2

echo "----- Installing Markdown -----"
pip install Markdown==3.4.4

echo "----- Installing Pilkit -----"
pip install pilkit==2.0

echo "----- Installing Pillow -----"
pip install Pillow==10.0.0

echo "----- Installing Six -----"
pip install six==1.16.0

echo "************************************************************"
echo "| Migrating Database                                       |"
echo "************************************************************"

echo "----- Tracking Project Changes -----"
python3 manage.py makemigrations

echo "----- Migrating Database -----"
python3 manage.py migrate

echo "----- Deactivating Virtual Enviroment -----"
deactivate

echo "************************************************************"
echo "| Finished.                                                |"
echo "| If everything went right, you should be able to run your |"
echo "| server now.                                              |"
echo "| Read Deployment section of the README for details.       |"
echo "************************************************************"
