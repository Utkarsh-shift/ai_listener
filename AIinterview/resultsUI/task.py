
import boto3
import os 
def start_ec2_instance():
    """
    Start an EC2 instance with specified AWS credentials, if it is not already running.
 
    :param instance_id: The ID of the EC2 instance to start.
    :param aws_access_key_id: Your AWS access key ID.
    :param aws_secret_access_key: Your AWS secret access key.
    :param region_name: The AWS region where the instance is located (default: 'ap-south-1').
    """
    # Create a session using provided AWS credentials and region
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
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
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
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
