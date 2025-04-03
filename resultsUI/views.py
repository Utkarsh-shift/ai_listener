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
    permission_classes=[IsAuthenticated,] 
    def post(self,request,*args , **kwargs ):
        from .serializers import LinkSerializer
        serializer = LinkSerializer(data=request.data)
        if serializer.is_valid():
            links1 = serializer.validated_data
            new_links=[]
            Id=[]
            Questions=[]
            batch_id=str(request.data["batch_id"])
            webhook_url = str(request.data["server_url"])
            print("###################The batch id received to listener is #######################" , batch_id)
            for item in links1["links"]:
                new_links.append(item["link"])
                Questions.append(item["question"])
            print("<<<<<<<<<<<<<<<<<<",json.dumps(request.data),">>>>>>>>>>>>>>>>>>") 
            if BatchEntry.objects.filter(batch_id=batch_id).exists():
                status_values = BatchEntry.objects.filter(batch_id=batch_id).values_list('status', flat=True)
                if str(status_values[0])=="processed":
                    results_values = BatchEntry.objects.filter(batch_id=batch_id).values_list('results', flat=True)

                    if results_values[0] is None:
                        print("################## The databases has stored the result as none ################")
                        LinkEntry.objects.filter(batch_id = batch_id).delete()
                        BatchEntry.objects.filter(batch_id = batch_id).delete()
                        start_ec2_instance.delay(data=request.data)
                        from datetime import datetime
                        created_at = datetime.utcnow().isoformat() + 'Z'
                        batch_id = request.data['batch_id']
                        res = {
                         "batch_id": batch_id,
                         "status": "received",
                         "created_at": created_at
                          }
                        return JsonResponse(res , safe=False)
                   
                     
                    else : 
                        result_final={"batch_id":batch_id,"status":"processed","data":results_values[0]}
                        print("The batch is found and is processed " , result_final)
                        return Response(result_final,status=status.HTTP_201_CREATED)
                
                if str(status_values[0])=="pending":
                    results_values = BatchEntry.objects.filter(batch_id=batch_id).values()[0]
                    filtered_data = {key: value for key, value in results_values.items() if key != "id"}
                    filtered_data1 = {key: value for key, value in filtered_data.items() if key != "results"}
                    return Response(filtered_data1,status=status.HTTP_201_CREATED)

                elif str(status_values[0]) == "failed" : 
                    print("Batch status is 'failed'. Deleting and restarting process.")
                    LinkEntry.objects.filter(batch_id=batch_id).delete()
                    BatchEntry.objects.filter(batch_id=batch_id).delete()
                    start_ec2_instance.delay(request.data)
                    created_at = datetime.utcnow().isoformat() + 'Z'
                    response_data = {
                        "batch_id": batch_id,
                        "status": "received",
                        "created_at": created_at
                    }
                    return JsonResponse(response_data, safe=False)
                
            else:
                print("lala")
                res = start_ec2_instance.delay(request.data)

                from datetime import datetime
                created_at = datetime.utcnow().isoformat() + 'Z'
                batch_id = request.data['batch_id']
                res = {
                        "batch_id": batch_id,
                        "status": "received",
                        "created_at": created_at
                    }
        
        return JsonResponse(res, safe=False)
    



