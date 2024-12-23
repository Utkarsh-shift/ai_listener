#!/bin/bash

# Restart Gunicorn
echo "Restarting Gunicorn service..."

# Reload Systemd Daemon
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Restart Gunicorn Socket and Service
echo "Restarting Gunicorn socket and service..."
sudo systemctl restart gunicorn.socket gunicorn.service

# Reload Nginx
echo "Reloading Nginx..."
sudo systemctl reload nginx

# Check the Status of Gunicorn
echo "Checking Gunicorn service status..."
sudo systemctl status gunicorn

echo "Checking Gunicorn socket status..."
sudo systemctl status gunicorn.socket

# Check the Status of Nginx
echo "Checking Nginx status..."
sudo systemctl status nginx

