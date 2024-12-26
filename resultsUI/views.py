# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import fileSerializers
# from rest_framework.permissions import IsAuthenticated
# from django.conf import settings
# from django.http import request,HttpResponse,JsonResponse
# from .models import interviewTest,interviewTest1
# import os
# import re, platform,threading
# from rest_framework_simplejwt.authentication import JWTAuthentication

# from .task import start_ec2_instance , stop_ec2_instance

# from django.http import JsonResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# import json

# import requests
# import json
# from decouple import config
# def trigger_webhook(api_url, bearer_token, payload):
#     headers = {
#         'Authorization': f'Bearer {config("BEARER_TOKEN")}',  # Bearer token for authentication
#         'Content-Type': 'application/json',  # Set content type to JSON
#     }
    
#     try:
#         print("Sending request to:", api_url)
#         print("Headers:", headers)
#         print("Payload:", payload)

#         response = requests.post(api_url, headers=headers, json=payload)
        
#         print("Response status code:", response.status_code)
#         print("Response body:", response.text)

#         return response.json() if response.headers.get("Content-Type") == "application/json" else {f"error": "Invalid response format {response}, maybe uuid is wrong"}
 
#     except requests.exceptions.Timeout:
#         return {"error": "Request timed out"}
#     except requests.exceptions.RequestException as err:
#         return {"error": f"Request error: {err}"}

            

# class uploadView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes=[IsAuthenticated,] # hold the process api until the request is server is available 

#     def post(self,request,format=None):

#         # print(request.data)
#         print("Here in the data wake up api call ")

#         data = request.data
#         batch_id = data.get("batch_id")
#         server_url = data.get("server_url")
#         links = data.get("links")

#         if not batch_id or not server_url or not links:
#             return JsonResponse({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

#         # Log the extracted data for debugging
#         print("Batch ID:", batch_id)
#         print("Server URL:", server_url)
#         print("Links:", links)

#         start_ec2_instance.delay(request=request)
#         from datetime import datetime
#         response_data = {
#             "batch_id": batch_id,
#             "status": "received",
#             "timestamp": datetime.now().isoformat()  # current timestamp in ISO format
#         }

        
        
       
#         print(response_data)  
            
#         return response_data.json() if response_data.headers.get("Content-Type") == "application/json" else {"error": "Invalid response format"}
 



from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.http import request,HttpResponse,JsonResponse
import os
import re, platform,threading
from rest_framework_simplejwt.authentication import JWTAuthentication

from .task import start_ec2_instance , stop_ec2_instance

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json
from .models import LinkEntry, BatchEntry
import requests
import json
from decouple import config

            

class uploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated,] # hold the process api until the request is server is available 

    def post(self,request,*args , **kwargs ):
        from .serializers import LinkSerializer
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            # print(serializer.validated_data)
            links1 = serializer.validated_data
            # print(links1)
            new_links=[]
            Id=[]
            Questions=[]
            batch_id=str(request.data["batch_id"])
            webhook_url = str(request.data["server_url"])
            for item in links1["links"]:
                # print("ID:", item["id"])
                # print("Link:", item["link"])
                # Id.append(item["id"])
                new_links.append(item["link"])
                Questions.append(item["question"])

            if BatchEntry.objects.filter(batch_id=batch_id).exists():
                status_values = BatchEntry.objects.filter(batch_id=batch_id).values_list('status', flat=True)
                if str(status_values[0])=="processed":
                    results_values = BatchEntry.objects.filter(batch_id=batch_id).values_list('results', flat=True)
                    result_final={"batch_id":batch_id,"status":"processed","data":results_values[0]}
                    print("The batch is found and is processed ")
                    return Response(result_final,status=status.HTTP_201_CREATED)
                if str(status_values[0])=="pending":
                    results_values = BatchEntry.objects.filter(batch_id=batch_id).values()[0]
                    filtered_data = {key: value for key, value in results_values.items() if key != "id"}
                    filtered_data1 = {key: value for key, value in filtered_data.items() if key != "results"}
                    return Response(filtered_data1,status=status.HTTP_201_CREATED)
                
            else:
                print("lala")
                res = start_ec2_instance.delay(data =request.data)

                from datetime import datetime
                created_at = datetime.utcnow().isoformat() + 'Z'
                batch_id = request.data['batch_id']
                res = {
                        "batch_id": batch_id,
                        "status": "pending",
                        "created_at": created_at
                    }
        
        return JsonResponse(res, safe=False)
    





# def trigger_webhook(api_url, bearer_token, payload):
#     headers = {
#         'Authorization': f'Bearer {config("BEARER_TOKEN")}',  # Bearer token for authentication
#         'Content-Type': 'application/json',  # Set content type to JSON
#     }
    
#     try:
#         print("Sending request to:", api_url)
#         print("Headers:", headers)
#         print("Payload:", payload)

#         response = requests.post(api_url, headers=headers, json=payload)
        
#         print("Response status code:", response.status_code)
#         print("Response body:", response.text)

#         return response.json() if response.headers.get("Content-Type") == "application/json" else {"error": "Invalid response format"}
 
#     except requests.exceptions.Timeout:
#         return {"error": "Request timed out"}
#     except requests.exceptions.RequestException as err:
#         return {"error": f"Request error: {err}"}
