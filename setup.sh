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

echo "Setup completed!"

# Install
echo "Running installation..."
./install.sh
