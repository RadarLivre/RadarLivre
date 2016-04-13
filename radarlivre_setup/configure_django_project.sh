echo "***************************************
* Configurando projeto django
***************************************";

BASEDIR=$(dirname "$0")
cd "$BASEDIR"
cd ..

sudo rm radarlivre_api/migrations/00* ;
sudo rm radarlivre_website/migrations/00* ;

source radarlivre_setup/venvs/django/bin/activate ;
sudo python manage.py makemigrations ;
sudo python manage.py migrate ;

echo "***************************************
* Configurando arquivos estáticos
***************************************";

sudo python manage.py collectstatic ;

echo "***************************************
* Adicionando usuário root
***************************************";

sudo python manage.py createsuperuser ;
