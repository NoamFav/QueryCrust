#!/bin/bash

# Define MySQL version
MYSQL_VERSION=mysql-apt-config_0.8.22-1_all.deb

# Update system
echo "Updating the system..."
sudo apt-get update

# Install wget if it's not installed
echo "Ensuring wget is installed..."
sudo apt-get install -y wget

# Download MySQL APT Config package
echo "Downloading MySQL APT Config package..."
wget https://dev.mysql.com/get/$MYSQL_VERSION

# Install the MySQL APT config package
echo "Installing MySQL APT Config package..."
sudo dpkg -i $MYSQL_VERSION

# Clean up the downloaded package
echo "Cleaning up downloaded files..."
rm $MYSQL_VERSION

# Update package information from MySQL APT repo
echo "Updating package lists from MySQL repositories..."
sudo apt-get update

# Install MySQL Server
echo "Installing MySQL Server..."
sudo apt-get install -y mysql-server

# Secure MySQL installation
echo "Securing MySQL installation..."
sudo mysql_secure_installation

# Print MySQL version
echo "MySQL installation completed. MySQL version:"
mysql --version
