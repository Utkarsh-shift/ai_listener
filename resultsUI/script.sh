#!/bin/bash

# Define your variables
REMOTE_USER="ubuntu"
REMOTE_HOST="10.0.8.162"
KEY_PATH="/home/ubuntu/DjangiAVItest/EC2kaypair.pem"
PROJECT_DIR="/home/ubuntu/AI_G"
CONDA_PATH="/home/ubuntu/anaconda3/etc/profile.d/conda.sh"
CONDA_ENV="s2"
DJANGO_PORT="0.0.0.0:8000"

# Connect to the remote server via SSH and run the commands
ssh -i "$KEY_PATH" "$REMOTE_USER@$REMOTE_HOST" << EOF
    # Initialize conda
    source "$CONDA_PATH"

    # Activate the specified conda environment
    conda activate "$CONDA_ENV"

    # Navigate to the project directory
    cd "$PROJECT_DIR"

    # Start Django server in the background and redirect output to a log file
    nohup python manage.py runserver "$DJANGO_PORT" > django_server.log 2>&1 &

    # Start Celery worker in the background and redirect output to a log file
    nohup celery -A your_project_name worker -l info > celery_worker.log 2>&1 &
EOF

echo "Commands executed on remote server $REMOTE_HOST"

