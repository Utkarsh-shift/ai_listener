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
        # Make the POST request with the provided URL, headers, and body (payload)
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Raise an error for any bad responses (optional, based on your error handling preferences)
        # response.raise_for_status()
        
        # Return the response JSON (or response text, depending on the API)
        return response.json()  # or response.text if the API does not return JSON
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except Exception as err:
        return {"error": f"Other error occurred: {err}"}


            

class uploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated,]

    def post(self,request,format=None):

        print(request.data) 
        # start_ec2_instance()
        brearer_token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI5Mjg0NTQ2LCJpYXQiOjE3MjkwNjg1NDYsImp0aSI6IjUwNWM0MjE2YTFkYjRlODk5NmY3MGVmZGNjOTVmZjkwIiwidXNlcl9pZCI6MX0.AasTYBYmyFk3E73sUE0vz_UGhnzI27uUfw89K9TkdGg"
        t=trigger_webhook("http://192.168.1.128/api/interviewTests",brearer_token,request.data)
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
