"""
import boto3
import os 

from decouple import config
def start_ec2_instance():
    
    Start an EC2 instance with specified AWS credentials, if it is not already running.
 
    :param instance_id: The ID of the EC2 instance to start.
    :param aws_access_key_id: Your AWS access key ID.
    :param aws_secret_access_key: Your AWS secret access key.
    :param region_name: The AWS region where the instance is located (default: 'ap-south-1').
    
    instance_id = config("INSTANCE_ID")
    aws_access_key_id = config("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")
    region_name = config("AWS_REGION", "ap-south-1")
    if not instance_id:
        raise ValueError("INSTANCE_ID environemnt varialbe is not set ")

    # Create a session using provided AWS credentials and region
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    
    ec2_client = session.client('ec2')
 
    try:
        # Describe the instance to check its state
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
 
        if instance_state == 'running':
            print(f'Instance {instance_id} is already running.')
            return None
 
        # Start the instance
        # hibernate param can be added see docs boto3 start instance
        start_response = ec2_client.start_instances(
            InstanceIds=[instance_id]
        )
        
        # Extract current and previous states from the response
        for instance in start_response['StartingInstances']:
            instance_id = instance['InstanceId']
            current_state = instance['CurrentState']
            previous_state = instance['PreviousState']
            
            print(f'Starting instance {instance_id}...')
            print(f'Current State: {current_state["Name"]}, Previous State: {previous_state["Name"]}')
 
        # Wait for the instance to be in the 'running' state
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        
        # Reload the instance state after starting
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
        print(f'Instance {instance_id} is now in {instance_state} state.')
 
    except Exception as e:
        print(f'Error starting instance {instance_id}: {e}')

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
    response = ec2_client.stop_instances(
    InstanceIds=[
        'string',
    ],
    Hibernate=True|False,
    DryRun=True|False,
    Force=True|False
)



"""




import boto3
import os
import time
from decouple import  config
import paramiko
import subprocess
def start_ec2_instance():
    
 
    instance_id = config("INSTANCE_ID")
    aws_access_key_id = config("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")
    region_name = config("AWS_REGION", "ap-south-1")

 
    if not instance_id:
        raise ValueError("INSTANCE_ID environment variable is not set.")

 
    print("Create a session")
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    
    ec2_client = session.client('ec2')
    ssm_client = session.client('ssm')

    try:
 
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if instance_state == 'running':
            print(f'Instance {instance_id} is already running.')
        else:
 
            print(f'Starting instance {instance_id}...')
            ec2_client.start_instances(InstanceIds=[instance_id])

            ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
            print(f'Instance {instance_id} is now running.')

            time.sleep(20)

            commands = [
                'echo piazzio > /home/ubuntu/spaceX123output.txt',
                'conda activate s2 ',  
                'cd /home/ubuntu/AI_G',  
                'sudo systemctl restart gunicorn',
                'sudo systemctl daemon-reload',
                'sudo systemctl restart gunicorn.socket gunicorn.service', 
                'nohup celery -A your_project_name worker -l info &' 
            ]

            print("The test here is *********************************************")
            ip = "10.0.8.162"
            ec2_user = "ubuntu"
            key_path = "/home/ubuntu/DjangiAVItest/EC2kaypair.pem"


            response = ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName="AWS-RunShellScript",
                Parameters={'commands': commands}
            )


            print("response is given as", response)
            command_id = response['Command']['CommandId']
            print(f"Command sent with Command ID: {command_id}")
            print("Django server and Celery worker are starting...")

    except Exception as e:
        print(f'Error initializing {instance_id}: {e}')


"""
import boto3
import time
import os
from decouple import  config
def start_ec2_instance():
    instance_id = "i-085b6360b8375d588"  # Replace with your instance ID
    region_name = "ap-south-1"  # Replace with your region if necessary
    instance_id = config("INSTANCE_ID")
    aws_access_key_id = config("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")
    region_name = config("AWS_REGION", "ap-south-1")
    # Initialize EC2 and SSM clients
    ec2_client = boto3.client('ec2', region_name=region_name)
    ssm_client = boto3.client('ssm', region_name=region_name)

    try:
        # Start the EC2 instance if it is not already running
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

        if instance_state != 'running':
            print(f"Starting instance {instance_id}...")
            ec2_client.start_instances(InstanceIds=[instance_id])

            # Wait for instance to fully start
            ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
            print(f"Instance {instance_id} is now running.")
        else:
            print(f"Instance {instance_id} is already running.")

        # Wait for the instance to be SSM-ready
        print("Checking if instance is SSM-ready...")
        for _ in range(10):  # Retry up to 10 times
            time.sleep(6)
            ssm_instances = ssm_client.describe_instance_information(
                Filters=[{'Key': 'InstanceIds', 'Values': [instance_id]}]
            ).get('InstanceInformationList', [])

            if ssm_instances:
                print("Instance is SSM-ready. Proceeding to send command.")
                break
        else:
            print("Instance is not SSM-ready. Exiting.")
            return

        # Send an SSM command if the instance is SSM-ready
        response = ssm_client.send_command(
            InstanceIds=[instance_id],
            DocumentName="AWS-RunShellScript",
            Parameters={'commands': ["echo 'Hello from SSM!'"]}
        )
        print("SSM command sent successfully:", response)

    except Exception as e:
        print(f"Error starting instance or sending command: {e}")

"""
