import boto3
import os
import time

import paramiko
import subprocess
import boto3
import time
from decouple import config


def stop_ec2_instance():
    instance_id = config("INSTANCE_ID")
    aws_access_key_id = config("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")
    region_name = config("AWS_REGION", "ap-south-1")
    

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    ec2_client = session.client('ec2')
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

    if instance_state == "running" : 

       
        response_instance = ec2_client.stop_instances(
        InstanceIds=[
            instance_id,
        ],
        Hibernate=False,
        DryRun=False,
        Force=False)
    else : 
        print(f'Instance {instance_id} is already running.')

    

    print(instance_state)






def start_ec2_instance():
    aws_access_key_id = config("AWS_ACCESS_KEY_ID")
    instance_id = config("INSTANCE_ID")
    aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")
    region_name = config("AWS_REGION", "ap-south-1")
    

    print(instance_id)

    if not instance_id:
        raise ValueError("INSTANCE_ID environment variable is not set.")

    print("Create a session")
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    print("Session created")

    ec2_client = session.client('ec2')
    ssm_client = session.client('ssm')

    try:
        print("Trying to send the describe_instance")
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if instance_state == 'running':
            print(f'Instance {instance_id} is already running. start_ec2_instance()' , instance_state)
        else:
            print(f'Starting instance {instance_id}...')
            ec2_client.start_instances(InstanceIds=[instance_id])
            ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
            print(f'Instance {instance_id} is now running.')

            time.sleep(20)

            env_name = config("ENV_NAME")
            commands = [
                'echo piazzio > /home/ubuntu/spaceX123output.txt',
                f'conda activate {env_name}',
                'cd /home/ubuntu/new_AVIPA',
                'sudo systemctl daemon-reload',
                'sudo systemctl restart gunicorn.socket',
                'sudo systemctl restart gunicorn.service',
                'sudo systemctl restart gunicorn',
                'sudo systemctl reload nginx',
                'sudo systemctl restart celery'
            ]

            print("Sending commands via SSM...")
            response = ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': commands}
            )

            print("Response is given as", response)
            command_id = response['Command']['CommandId']
            print(f"Command sent with Command ID: {command_id}")
            print("Django server and Celery worker are starting...")

    except Exception as e:
        print(f'Error initializing {instance_id}: {e}')

# def main():
#     try:
#         print("Starting EC2 instance setup process...")
#         start_ec2_instance()
#         #stop_ec2_instance()
#         print("EC2 instance setup process completed.")
#     except Exception as e:
#         print(f"An error occurred in the main function: {e}")

# if __name__ == "__main__":
#     main()