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

class uploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes=[IsAuthenticated,]
    # print(authentication_classes,permission_classes)
    def post(self,request,format=None):
        serializer = fileSerializers(data=request.data)
        # print(serializer)
        if serializer.is_valid():
            uploadedFile=serializer.save()
            filePath = os.path.join(settings.MEDIA_ROOT,str(uploadedFile.file.name).replace(" ","_"))
        return HttpResponse("hello")

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

        
#         # print(filepath)
#         try:
#             fileName=''
#             # print("9")

#             resume = main(filepath,0)
#             # print(resume)
#             if type(resume)==type(['a','b']):
#                 finalResponse=[]
#                 for x in range(len(resume)):
#                     fileName=''
#                     time=''
#                     pre_fetch={}
#                     var = resume[x]
#                     responseData1={}
#                     responseData=[]
#                     if type(var)==type(('a',1)):    
#                         finalResponse.append({'status' :status.HTTP_400_BAD_REQUEST,'file_name':var[0].split("\\")[-1],"extraction_Time": var[1],'data':[]})
#                         continue
#                     for i in var :#range(len(var)):
#                         # print(var[i])
#                         if i=='file_name':
#                             fileName=var[i].split("\\")[-1]
#                             continue
#                         elif i=='extraction_time':
#                             time = var[i]
#                             continue
#                         if type(var[i])== None:
#                             responseData.append(f"{i} : 'Not Available'")
#                             pre_fetch[i] = "Not Available"
#                             # print("1")
#                             continue
#                         if var[i] and len(var[i])>1:
#                             extractingData=[]
#                             if type(var[i])==type(['a','b']) or type(var[i])==type((1,2)):
#                                 # print("2")
#                                 for j in range(len(var[i])):
#                                     extractingData.append(var[i][j])
#                                 responseData.append({i:extractingData})
#                                 pre_fetch[i] = extractingData
#                             elif type(var[i])==type("Hello"):
#                                 responseData.append({i:var[i]})
#                                 pre_fetch[i] = var[i]
#                             elif type(var[i]==type({'a':1,'b':2})):
#                                 # print('3')
#                                 # for j in var[i]:
#                                 #     extractingData.append({j : var[i][j]})
#                                 responseData.append({i:var[i]})
#                                 pre_fetch[i] = var[i]
#                         else:
#                             # print('4')
#                             pre_fetch[i] = var[i]
#                     # else:
#                     responseData1[fileName]={'Status' : status.HTTP_200_OK,"Extraction_Time": time,'data':pre_fetch}
#                         # responseData1 = ['Status':]
#                     finalResponse.append(responseData1)
#                 # response= JsonResponse(resume,safe=False)
#                 # pretty_json = json.dumps(json.loads(response.content), indent=4)
#                 return JsonResponse(finalResponse, safe=False)
#             else:
#                 # if 
#                 # responseData1=['Status : Success',]
#                 responseData=[]
#                 try:
#                     pre_dict={}
#                     time=''
#                     if type(resume)==type((1,2)):
#                         fileName = resume[0].split("\\")[-1]
#                         time = resume[1]
#                         x=1/0
#                     for i in resume:
#                         if i=='file_name':
#                             fileName=resume[i].split("\\")[-1]
#                             continue
#                         if type(resume[i])== None:
#                             responseData.append(f"{i} : 'Not Available'")
#                             pre_dict[i]='Not Available'
#                             # print("5")
#                             continue
#                         if resume[i] and len(resume[i])>1:
#                             extractingData=[]
#                             if type(resume[i])==type(['a','b']) or type(resume[i])==type((1,2)):
#                                 # print("6")
#                                 for j in range(len(resume[i])):
#                                     extractingData.append(resume[i][j])
#                                 responseData.append(list({i:extractingData}.items()))
#                                 pre_dict[i]=extractingData
#                             elif type(resume[i])==type("Hello"):
#                                 responseData.append({i:resume[i]})
#                                 pre_dict[i]=resume[i]
#                             elif type(resume[i]==type({'a':1,'b':2})):
#                                 # print('7')
#                                 # for j in resume[i]:
#                                 #     extractingData.append({j : resume[i][j]})
#                                 responseData.append({i:resume[i]})
#                                 pre_dict[i]=resume[i]
                            
#                         else:
#                             # print('8')
#                             responseData.append({i:resume[i]})
#                             pre_dict[i]=resume[i]
#                             # responseData.append({i:resume[i]})
#                         # print(responseData)
#                     dictionary={'Status':status.HTTP_200_OK,'file_Name':fileName,"Extraction_Time": datetime.now().strftime("%H:%M:%S"),'data':pre_dict}
#                     # result = dictionary.items()
#                     # responseData1 = result
#                     return JsonResponse(dictionary)
#                 except Exception as e:
#                     print(f"2 {e}")
#                     return JsonResponse({'Status':status.HTTP_400_BAD_REQUEST,'file_Name':fileName,'Extraction_Time':datetime.now().strftime("%H:%M:%S"),'data':[]},safe=False)
#         except Exception as e:
#             print(f"3 {e}")
#             return HttpResponse("Error extracting resume")
#     return render(request,"Home.html")
# # count=0
# # def 
# def main(fileName,flag):
#     logger = logging.getLogger(__name__)
#     try:
#         # fileName = os.path.join(settings.BASE_DIR,"savedModels/1.pdf")
#         #opening a file
#         extText=''
#         # if fileName.split(".")[1]=='pdf':
#         #     extText = getText(readingBounds(reader,readData(fileName)))
#         # else:
#         #     extText = getText(readingBounds(reader,readData(pdfConvert(fileName))))
        
#         if fileName.split(".")[-1]=='pdf':
#             try:
#                 extText = "\n ".join(rf.removingExtraSpace(rf.readPDF(fileName)))
#                 # extText = rf.readPDF(fileName)
#                 print(f"{fileName}-------------{len(extText)}")
#                 if extText==None or len(extText)==0:
#                     reader = easyocr.Reader(['en'],gpu=True)
#                     extText = rf.getText(rf.readingBounds(reader,rf.readData(fileName)))
#                     # print(len(extText))

#             except:
#                 extText = rf.getText(rf.readingBounds(reader,rf.readData(fileName)))
#         elif fileName.split(".")[1]=='docx':
#             if platform.system()=="Windows":
#                 try:
#                     extText = "\n ".join(rf.removingExtraSpace(rf.readPDF(rf.pdfConvert(fileName))))
#                     if extText==None:
#                         reader = easyocr.Reader(['en'],gpu=True)
#                         extText = rf.getText(rf.readingBounds(reader,rf.readData(rf.pdfConvert(fileName))))            
#                 except:
#                     reader = easyocr.Reader(['en'],gpu=True)
#                     extText = rf.getText(rf.readingBounds(reader,rf.readData(rf.pdfConvert(fileName))))
#             elif platform.system()=="Linux":
#                 try:
#                     extText = "\n ".join(rf.removingExtraSpace(rf.readPDF(rf.pdfConvertLinux(fileName))))
#                     if extText==None:
#                         reader = easyocr.Reader(['en'],gpu=True)
#                         extText = rf.getText(rf.readingBounds(reader,rf.readData(rf.pdfConvertLinux(fileName))))            
#                 except:
#                     reader = easyocr.Reader(['en'],gpu=True)
#                     extText = rf.getText(rf.readingBounds(reader,rf.readData(rf.pdfConvertLinux(fileName))))
#         else:
#             # path = extract_file(fileName)
#             ls=[]
#             if fileName.split(".")[-1]!='zip':
#                 return(fileName,datetime.now().strftime("%H:%M:%S"),None)
#             path = rf.extract_file(fileName)
            
#             # path = os.path.join(os.getcwd(),path)
#             if os.path.isdir(path):
#                 dir = os.listdir(path)
#                 flag=1
#                 for i in dir:
#                     if os.path.isdir(os.path.join(path,i)):
#                         pass
#                     else:
#                         filePath = os.path.join(path,i)
#                         ls.append(main(filePath,flag))
#                 return ls
#             else:
#                 return main(path,flag)
#         # extText = rf.cleanResume(extText)
#         #fetching Name 
#         fetchedResume = GPTCall(extText)
#         fetchedResume['file_name'] = fileName
#         try:
#             return fetchedResume
#         except Exception as e:
#             print(e)
#         # extText = extText.replace("Email","")
#         # Name = rf.FetchName(rf.cleanResume(extText))
#         # if Name==None:
#         #     Name = rf.extract_name(extText)
#         #     if Name==None:
#         #         extText = rf.getText(rf.readingBounds(rf.reader,rf.readData(fileName)))
#         #         Name = rf.extract_name(extText)
#         # # try:
#         # #     Name = rf.NormalizeName(rf.fixName(Name))

#         # # except:
#         # Name = rf.NormalizeName(Name)            
#         # # except Exception as e:
#         #     # print(e)
        
#         # carreerProfile = " ".join(rf.extractCarrerProfile(extText,0))

        
#         # #fetching Email and contact
#         # contact = rf.extractContact(extText.replace("\n"," "))
#         # email = rf.extractEmail(extText)

#         # dateList=[]
#         # #fetching work History
#         # workExperience = rf.extractWorkHistory(extText,0)
#         # if workExperience==None:
#         #     workExperience,dateList = rf.extractPastWorkExperience(extText)
#         # else:
#         #     workExperience,dateList = rf.extractPastWorkExperience(workExperience)
#         # # print(dateList)
#         # expCount=''
#         # try:
#         #     if dateList:
#         #         expCount = rf.experienceCount(dateList)
#         #         print(expCount)
#         #         dateList.clear()
#         # except Exception as e:
#         #     print(f"Experience Count error {e}")
#         # #extracting skills
#         # skills = rf.FetchModelSkills(rf.cleanResume(extText))
        
#         # #fetching Links
#         # socialLinks = rf.extract_SocialLinks(extText)
#         # linkedIn = rf.FetchLinkedIn(extText)
        
        
#         # #education complexities
#         # education=rf.extractAcademicDetails(extText,0)
#         # eFlag=0
#         # if education==None:
#         #     education = rf.extractAcademicDetails(extText,0)
#         #     if education==None:
#         #         education = rf.FetchEducation(extText)
#         #         eFlag=1
#         # if eFlag!=1:
#         #     education=rf.FetchEducation(education)
#         #     if education==None:
#         #         education = rf.FetchEducation(extText)

        
#         # #project Complexitites
#         # projects = rf.extractProjects(extText,0)
#         # if projects==None:
#         #     projects = rf.FetchProjects(extText)
#         # else:
#         #     if rf.FetchProjects(projects)==None:
#         #         projects = rf.FetchProjects(extText)
#         #     else:
#         #         projects = rf.FetchProjects(projects)

#         # #Fetching Languages
#         # languages = rf.extractLanguages(extText)
#         # location = rf.findLoc(extText)
#         # if flag==0:

#         #     dictionary = {'file_name':fileName,"name":Name,"contact_info":{"mobile_no":contact,"email":email},"location":location,"linkedin_profile":linkedIn,"experience":expCount,"skills":skills,"summary":rf.cleanResume1(carreerProfile),"projects":projects,"education":education,"work_experience":workExperience,"certifications":rf.extractCertifications(extText,0),"social_links":socialLinks,"languages":languages}
#         # else:
#         #     dictionary = {'file_name':fileName,"extraction_time":datetime.now().strftime("%H:%M:%S"),"name":Name,"contact":[contact,email],"location":location,"linkedin_profile":linkedIn,"experience":expCount,"skills":skills,"summary":rf.cleanResume1(carreerProfile),"projects":projects,"education":education,"work_experience":workExperience,"certifications":rf.extractCertifications(extText,0),"social_media":socialLinks,"languages":languages}
#         # print(cleanResume(extText)
#         # return JsonResponse(dictionary)
#         logger.info("A JSON of extracted data is ready.")
#         # return dictionary

#     except Exception as e:
#         logger.error(f"Exception {e} is occured in main function.")

# def ERROR_RESPONSE(request):
#     response={
#         'error': 'Internal Server Error',
#         'status_code': '500'
#     }
#     return JsonResponse(response)

# def ERROR_404(request,exception):
#     response={
#         'error': 'Not Found',
#         'status_code': '404'
#     }

#     return JsonResponse(response,status=404)
