#!/bin/bash

# Configure PostgreSQL
echo "Configuring PostgreSQL..."
sudo sed -i 's/port = 5432/port = 5431/g' /etc/postgresql/*/main/postgresql.conf 2>/dev/null || echo "PostgreSQL config not found, continuing..."
sudo service postgresql restart

# Configure PostgreSQL password
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null || echo "Password already set, continuing..."

# Create database
echo "Creating database..."
sudo -u postgres psql -c "CREATE DATABASE radarlivre;" 2>/dev/null || echo "Database already exists, continuing..."
sudo -u postgres psql -d radarlivre -c "CREATE EXTENSION IF NOT EXISTS postgis; CREATE EXTENSION IF NOT EXISTS postgis_topology;" 2>/dev/null || echo "Extensions already exist, continuing..."

echo "Setup completed!"

# Install
echo "Running installation..."
./install.sh


./setup.sh
