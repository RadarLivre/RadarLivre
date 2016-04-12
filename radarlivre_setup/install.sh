BASEDIR=$(dirname "$0")
cd "$BASEDIR"

chmod +x *.sh

./install_dependencies.sh
./create_virtual_env.sh
./create_project_dirs.sh