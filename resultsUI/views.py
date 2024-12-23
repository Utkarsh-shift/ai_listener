from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import fileSerializers
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import request,HttpResponse,JsonResponse
from .models import interviewTest,interviewTest1
import os
import re, platform,threading
from rest_framework_simplejwt.authentication import JWTAuthentication

from .task import start_ec2_instance , stop_ec2_instance

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

import requests
import json
from decouple import config
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

        return response.json() if response.headers.get("Content-Type") == "application/json" else {"error": "Invalid response format"}
 
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request error: {err}"}

            

class uploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated,] # hold the process api until the request is server is available 

    def post(self,request,format=None):

        print(request.data)
        print("Here in the data wake up api call ")
        start_ec2_instance()
        brearer_token=config("BEARER_TOKEN")
        t = None
        try:
            t = trigger_webhook(config("SERVER_2_URL"), brearer_token, request.data)
            print("In try block of trigger webhook", t)
        except Exception as e:
            print(f"Exception occurred during webhook triggering: {e}")
            try:
                t = trigger_webhook(config("SERVER_2_URL"), brearer_token, request.data)
                print("In exception trigger webhook block", t)
            except Exception as retry_exception:
                print(f"Retry failed: {retry_exception}")
                t = {"error": "Webhook trigger failed after retry."}
        finally:
            # stop_ec2_instance()
            print("The engine has to be stopped ")
            pass
        
        return JsonResponse(t)