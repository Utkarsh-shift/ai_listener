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
        response = requests.post(api_url, headers=headers, json=payload, timeout=10)
        
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
        brearer_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU5ODYzMTExLCJpYXQiOjE3MzEwNjMxMTEsImp0aSI6ImYxYTJmZmZkZGQ5YjRjODNhZTE4YjkyMTVlMGY1NTBlIiwidXNlcl9pZCI6MX0.FPdBmcYAmHhgR9Sycfu_IIVgcW-ECx59XC0qJY86328"
        try:
            t=trigger_webhook("http://10.0.8.162/api/interviewTest",brearer_token,request.data)
            print(t)
        except:
            t=trigger_webhook("http://65.0.92.35/api/interviewTest",brearer_token,request.data)
            print(t)
        return JsonResponse(t)



# Create your views here. 
def Welcome(request):
    
    if request.method == "POST":
        if 'File' not in request.FILES:
            return HttpResponse("Error: No file uploaded.")

        file1 = request.FILES["File"]
        file1.name = file1.name.replace(" ","_")
        file1.name = re.sub(r'[^\w.-]',"",file1.name)
        # pattern =r"[^a-zA-Z0-9\s]"
        # file1.name = re.sub(pattern,'',file1.name)
        filepath = os.path.join(settings.MEDIA_ROOT, str(file1.name).replace(" ","_"))
        
        # Storing file on server
        document = interviewTest1.objects.create(file=file1)
        document.save()
    return render(request,"Home.html")
