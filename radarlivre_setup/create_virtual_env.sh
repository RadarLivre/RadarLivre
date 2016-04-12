BASEDIR=$(dirname "$0")
cd "$BASEDIR"

sudo apt-get install python-virtualenv

virtualenv venvs/django

source venvs/django/bin/activate

pip install django
