from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import fileSerializers
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
# # import parser.resumeFunction as rf
from django.http import request,HttpResponse,JsonResponse
# # import os,easyocr,logging
# from django.conf import settings
from .models import interviewTest,interviewTest1
# from datetime import datetime
import os
import re, platform,threading
from rest_framework_simplejwt.authentication import JWTAuthentication
# # from .Gpt import GPTCall

from .task import start_ec2_instance

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

import requests
import json
from decouple import config
def trigger_webhook(api_url, bearer_token, payload):
    headers = {
        'Authorization': f'Bearer {bearer_token}',  # Bearer token for authentication
        'Content-Type': 'application/json',  # Set content type to JSON
    }
    
    try:
        print("Sending request to:", api_url)
        print("Headers:", headers)
        print("Payload:", payload)
        
        # Make the POST request
        response = requests.post(api_url, headers=headers, json=payload)
        
        print("Response status code:", response.status_code)
        print("Response body:", response.text)
        
        # Check if the response is JSON
        return response.json() if response.headers.get("Content-Type") == "application/json" else {"error": "Invalid response format"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Request error: {err}"}

            

class uploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated,]

    def post(self,request,format=None):

        print(request.data)
        print("Here in the data wake up api call ")
        start_ec2_instance()
        brearer_token=config("BEARER_TOKEN")
        try:
            t=trigger_webhook(config("SERVER_2_URL"),brearer_token,request.data)
            print("In try block of trigger webhook",t)
        except:
            t=trigger_webhook(config("SERVER_2_URL"),brearer_token,request.data)
            print("in exception trigger webhook block",t)
        return JsonResponse(t)



