#!/bin/bash

echo "Restarting Gunicorn service..."

echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Restarting Gunicorn socket and service..."
sudo systemctl restart gunicorn.socket gunicorn.service

sudo systemctl restart celery

echo "Reloading Nginx..."
sudo systemctl reload nginx
