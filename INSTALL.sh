#/bin/bash
# The command above states wich shell is used

# This file is used to set up the project installing all requirements and dependencies
# Keep it as automated as possible, as the software must be easy enough for everyone to install
# Use ----- <Description> ----- to help users track installation proccess and possible errors.

# Every step is divided in sections as the following, so it is easier to track error and program

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
sudo apt-get install python-virtualenv

echo "----- Installing SQLite -----"
sudo apt-get install sqlite3 libsqlite3-dev

echo "************************************************************"
echo "| Creating Virtual Enviroment                              |"
echo "************************************************************"

virtualenv env

echo "************************************************************"
echo "| Configuring Virtual Enviroment                           |"
echo "************************************************************"

echo "----- Activating virtual enviroment -----"
source env/bin/activate

# The next steps will be executed while the virtual enviroment is activated.
# As Django comes with Pip installed, there is no need to install it.

echo "************************************************************"
echo "| Installing Virtual Enviroment Requirements               |"
echo "************************************************************"

echo "----- Installing Appdirs -----"
pip install appdirs==1.4.3

echo "----- Installing Django -----"
pip install Django==1.9.4

echo "----- Installing Django Appconf -----"
pip install django-appconf==1.0.1

echo "----- Installing Django Cleanup -----"
pip install django-cleanup==0.4.2

echo "----- Installing Django Crispy Forms -----"
pip install django-crispy-forms==1.6.1

echo "----- Installing Django Filter -----"
pip install django-filter==1.0.1

echo "----- Installing Django Imagekit -----"
pip install django-imagekit==3.3

echo "----- Installing Django Rest -----"
pip install django-rest==0.0.1

echo "----- Installing Django Rest Framework -----"
pip install djangorestframework==3.5.3

echo "----- Installing Django Rest Framework Jsonp -----"
pip install djangorestframework-jsonp==1.0.2

echo "----- Installing Markdown -----"
pip install Markdown==2.6.7

echo "----- Installing Pilkit -----"
pip install pilkit==1.1.13

echo "----- Installing Pillow -----"
pip install Pillow==3.4.2

echo "----- Installing Six -----"
pip install six==1.10.0

echo "************************************************************"
echo "| Migrating Database                                       |"
echo "************************************************************"

echo "----- Tracking Project Changes -----"
python manage.py makemigrations

echo "----- Migrating Database -----"
python manage.py migrate

echo "----- Deactivating Virtual Enviroment -----"
deactivate

echo "************************************************************"
echo "| Finished.                                                |"
echo "| If everything went right, you should be able to run your |"
echo "| server now.                                              |"
echo "| Read Deployment section of the README for details.       |"
echo "************************************************************"