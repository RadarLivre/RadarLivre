echo "***************************************
* Instalando dependencias django
***************************************";

sudo apt-get update ;
sudo apt-get -y install apache2 libapache2-mod-wsgi ;

sudo apt-get -y install python-dev python-setuptools ;
sudo apt-get -y install libjpeg8-dev ;
sudo apt-get -y install zlib1g-dev ;
sudo apt-get -y install libtiff5-dev ;
sudo apt-get -y install libfreetype6-dev ;
sudo apt-get -y install liblcms2-dev ;
sudo apt-get -y install libwebp-dev ;
sudo apt-get -y install tcl8.6-dev ;
sudo apt-get -y install tk8.6-dev ;
sudo apt-get -y install python-tk ;
sudo apt-get install postgresql-server-dev-9.5;
