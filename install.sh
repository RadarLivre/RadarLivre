BASEDIR=$(dirname "$0")
cd "$BASEDIR";

sudo chmod +x *.sh;

sudo ./unistal.sh
sudo ./radarlivre_setup/install_dependencies.sh;
sudo ./radarlivre_setup/create_virtual_env.sh;
sudo ./radarlivre_setup/install_requeriments.sh;
sudo ./radarlivre_setup/create_project_dirs.sh;
sudo ./radarlivre_setup/create_apache_config.sh;
sudo ./radarlivre_setup/configure_django_project.sh
