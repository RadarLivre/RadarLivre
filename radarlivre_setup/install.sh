BASEDIR=$(dirname "$0")
cd "$BASEDIR"

chmod +x *.sh

./install_dependencies.sh
./create_virtual_env.sh
./install_requeriments.sh
./create_project_dirs.sh
./create_apache_config.sh
./configure_django_project.sh
