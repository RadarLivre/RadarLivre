echo "***************************************
* Criando ambiente virtual python
***************************************";

BASEDIR=$(dirname "$0")
cd "$BASEDIR"

sudo apt-get install python-virtualenv ;

virtualenv venvs/django
