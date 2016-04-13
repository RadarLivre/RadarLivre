echo "***************************************
* Criando diretórios do projeto
***************************************";

BASEDIR=$(dirname "$0")
cd "$BASEDIR"

mkdir -p ../log ;
touch ../log/radarlivre.log
mkdir -p ../static ;
mkdir -p ../media ;
mkdir -p ../database ;
chmod 775 ../* -R ;
chmod 777 ../log ;
chmod 777 ../log/radarlivre.log
chmod 777 ../static ;
chmod 777 ../media ;
chmod 777 ../database
