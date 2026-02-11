#!/bin/bash

# Install PostGIS system package
echo "Installing PostGIS..."
sudo apt-get install -y postgresql-16-postgis-3 2>/dev/null || echo "PostGIS installation failed or already installed"

# Configure PostgreSQL
echo "Configuring PostgreSQL..."

# Check if PostgreSQL is running
if systemctl is-active --quiet postgresql; then
    echo "PostgreSQL is already running, stopping first..."
    sudo service postgresql stop
fi

# Change port (only if file exists)
if [ -f /etc/postgresql/*/main/postgresql.conf ]; then
    sudo sed -i 's/port = 5432/port = 5431/g' /etc/postgresql/*/main/postgresql.conf
    echo "PostgreSQL port changed to 5431"
else
    echo "PostgreSQL config not found, skipping port change..."
fi

# Start PostgreSQL
echo "Starting PostgreSQL..."
sudo service postgresql start
sleep 3  # Give it time to start

# Configure PostgreSQL password
echo "Setting PostgreSQL password..."
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null && echo "Password set" || echo "Password already set or failed"

# Create database
echo "Creating database..."
sudo -u postgres psql -c "CREATE DATABASE radarlivre;" 2>/dev/null && echo "Database created" || echo "Database already exists"

# Create extensions
echo "Creating PostGIS extensions..."
sudo -u postgres psql -d radarlivre -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS postgis_topology;" 2>/dev/null && echo "Extensions created" || echo "Extensions already exist or failed"

# Install Apache and its required modules
echo "Installing and configuring Apache as Reverse Proxy..."
sudo apt install apache2 libapache2-mod-wsgi-py3 -y

# Apply required modules
sudo a2enmod proxy proxy_http rewrite headers

# Configure ServerName to avoid error
echo "ServerName localhost" | sudo tee /etc/apache2/conf-available/servername.conf
sudo a2enconf servername.conf

# Create Apache config file
CURRENT_DIR=$(pwd)
cat <<EOF | sudo tee /etc/apache2/sites-available/radarlivre.conf
<VirtualHost *:80>
    ServerName localhost
    ServerAlias 127.0.0.1

	Header always set X-Proxied-By "Apache-2.4-ReverseProxy"

    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/

    Alias /static ${CURRENT_DIR}/static
    <Directory ${CURRENT_DIR}/static>
        Require all granted
    </Directory>

    Alias /media ${CURRENT_DIR}/media
    <Directory ${CURRENT_DIR}/media>
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

# Activate config
sudo a2ensite radarlivre.conf
sudo a2dissite 000-default.conf

# Test config before restarting
if sudo apache2ctl configtest; then
    echo "Configuring was successfull! Restarting Apache..."
    sudo systemctl restart apache2
else
    echo "ERROR on the Apache configuring. Check the logs."
    exit 1
fi

echo "Apache configurated successfully!"

echo "Setup completed!"

# Install
echo "Running installation..."
./install.sh
