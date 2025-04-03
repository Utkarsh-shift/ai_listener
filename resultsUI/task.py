import boto3
import os
import time
from celery import shared_task
import paramiko
import subprocess
import boto3
import time
from decouple import config
import requests
from celery import current_app
from django.db import connection
import json
def trigger_webhook(api_url, bearer_token, payload):
    headers = {
        'Authorization': f'Bearer {config("BEARER_TOKEN")}',  # Bearer token for authentication
        'Content-Type': 'application/json',  # Set content type to JSON
    }
    
    try:
        print("Sending request to:", api_url)
        print("Headers:", headers)
        print("Payload:", payload)

        response = requests.post(api_url, headers=headers, json=payload)
        
        print("Response status code:", response.status_code)
        print("Response body:", response.text)

        return response.json() if response.headers.get("Content-Type") == "application/json" else {f"error": "Invalid response format {response}"}
 
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request error: {err}"}



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
        instance_stopped_waiter = ec2_client.get_waiter('instance_stopped')
        instance_stopped_waiter.wait(InstanceIds=[instance_id])
        print(f'Instance {instance_id} is stopped.')
    else : 
        print(f'Instance {instance_id} is already running.')
    print(instance_state)


@shared_task(bind=True)
def start_ec2_instance(self,data):
    print("********************************************************************************************")
 # Extract task metadata
    task_id = self.request.id
    task_name = self.name
    worker_name = self.request.hostname  # Fixed typo here
    task_args = json.dumps(self.request.args) if self.request.args else "[]"
    task_kwargs = json.dumps(self.request.kwargs) if self.request.kwargs else "{}"

    # Debugging prints
    print(current_app.conf.result_backend)
    print(f"🔹 Task ID: {task_id}")
    print(f"🔹 Task Name: {task_name}")
    print(f"🔹 Worker Name: {worker_name}")
    print(f"🔹 Task Arguments: {task_args}")
    print(f"🔹 Task Keyword Arguments: {task_kwargs}")

    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM django_celery_results_taskresult WHERE task_id = %s", [task_id])
        task_exists = cursor.fetchone()[0]

        if task_exists:
       
            sql = """
                UPDATE django_celery_results_taskresult
                SET task_name = %s, worker = %s, task_args = %s, task_kwargs = %s
                WHERE task_id = %s
            """
            cursor.execute(sql, [task_name, worker_name, task_args, task_kwargs, task_id])
           


    print(f"Starting EC2 Instance with data: {data}")
    aws_access_key_id = config("AWS_ACCESS_KEY_ID")
    instance_id = config("INSTANCE_ID")
    aws_secret_access_key = config("AWS_SECRET_ACCESS_KEY")
    region_name = config("AWS_REGION", "ap-south-1")
    
    print(instance_id)

    if not instance_id:
        raise ValueError("INSTANCE_ID environment variable is not set.")
    time.sleep(30)
    print("Create a session")
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    print("Session created")

    ec2_client = session.client('ec2')
    ssm_client = session.client('ssm')
    result = None
    time.sleep(5)
    try:
        print("Trying to send the describe_instance")
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

        print("The currect state for instace is ", instance_state)
        time.sleep(5)

        if instance_state == 'running':
            print(f'Instance {instance_id} is already running. start_ec2_instance()' , instance_state)

            brearer_token=config("BEARER_TOKEN")
            
            try:
                print("##############",data)
                result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                print("In try block of trigger webk", result)
            except Exception as e:
                print(f"Exception occurred during webhook triggering: {e}")
                try:
                    result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                    print("In exception trigger webhook block", result)
                except Exception as retry_exception:
                    print(f"Retry failed: {retry_exception}")
                    result = {"error": "Webhook trigger failed after retry."}
            return result

        elif instance_state == 'stopping' or instance_state == "shutting-down":

            time.sleep(120)

            print(f'Instance {instance_id} is in {instance_state} state. Waiting for it to stop...')

            instance_stopped_waiter =ec2_client.get_waiter('instance_stopped')
            print("The waiter is  ", instance_stopped_waiter)
            instance_stopped_waiter.wait(InstanceIds = [instance_id])
            print(f'Instance {instance_id} is now stopped. Starting it...')

            print(f'Starting instance {instance_id}...')
            ec2_client.start_instances(InstanceIds=[instance_id])
            instance_running_waiter = ec2_client.get_waiter('instance_running')
            print("The running waiter is " , instance_running_waiter)
            instance_running_waiter.wait(InstanceIds= [instance_id])
            # print(f'Instance{instance_id} is now started. sending the ssm messages')
           
            time.sleep(60)
            response = ec2_client.describe_instances(InstanceIds=[instance_id])
            instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
            time.sleep(60)

            # celery retry mechanism to cheak if the instance is really running or not 
            brearer_token=config("BEARER_TOKEN")
          
            try:
                print("##############",data)
                result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                print("In try block of trigger webhook", result)
            except Exception as e:
                print(f"Exception occurred during webhook triggering: {e}")
                try:
                    result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                    
                except Exception as retry_exception:
                    print(f"Retry failed: {retry_exception}")
                    result = {"error": "Webhook trigger failed after retry."}

        elif instance_state == 'pending':
            print(f'Instance {instance_id} is in initializing (pending) state. Waiting for it to be running...')
            instance_running_waiter = ec2_client.get_waiter('instance_running')
            instance_running_waiter.wait(InstanceIds=[instance_id])

            # celery retry mechnism to be added here to check the instance -state of the process , if it is really runnign or not 
            print(f'Instance {instance_id} is now running.')
            time.sleep(60)


            brearer_token=config("BEARER_TOKEN")
           
            try:
                print("##############",data)
                result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                print("In try block of trigger webhook", result)
            except Exception as e:
                print(f"Exception occurred during webhook triggering: {e}")
                try:
                    result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                    print("In exception trigger webhook block", result)
                except Exception as retry_exception:
                    print(f"Retry failed: {retry_exception}")
                    result = {"error": "Webhook trigger failed after retry."}

          #  send_ssm_command(instance_id , ssm_client)
        elif instance_state == 'stopped':
            print(f"Instance {instance_id} is already stopped. Proceeding with command execution.")
            print(f'Starting instance {instance_id}...')
            ec2_client.start_instances(InstanceIds=[instance_id])
            instance_running_waiter = ec2_client.get_waiter('instance_running')
            print(instance_running_waiter)
            instance_running_waiter.wait(InstanceIds= [instance_id])
            print(f'Instance {instance_id} is now running.')
            time.sleep(60)
            brearer_token=config("BEARER_TOKEN")
            try:
                print("##############",data)
                result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                print("In try block of trigger webhook", result)
            except Exception as e:
                print(f"Exception occurred during webhook triggering: {e}")
                try:
                    result = trigger_webhook(config("SERVER_2_URL"), brearer_token, data)
                    print("In exception trigger webhook block", result)
                except Exception as retry_exception:
                    print(f"Retry failed: {retry_exception}")
                    result = {"error": "Webhook trigger failed after retry."}
    except Exception as e:
        print(f'Error initializing {instance_id}: {e}')




def getstatus():
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
    print("Trying to send the describe_instance")
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']

    print("The currect state for instace is ", instance_state)




def main():
    try:
        print("Starting EC2 instance setup process...")
        data = None
        start_ec2_instance(data)
        print("EC2 instance setup process completed.")
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()