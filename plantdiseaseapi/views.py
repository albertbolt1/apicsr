from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import PlantDiseaseImageSerializer
from django.http.response import JsonResponse
import mediapipe as mp
import cv2
import numpy as np
import uuid
import os
import numpy as np
from PIL import Image
from numpy import asarray
import math
import os
from django.shortcuts import render,redirect
 
# Function to find distance
def distance(x1, y1, z1, x2, y2, z2):
    d = math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) +
                math.pow(z2 - z1, 2)* 1.0)
    return d



class MyImageView(APIView):
		parser_classes = (MultiPartParser, FormParser)
		def post(self, request, *args, **kwargs):
				serializer = PlantDiseaseImageSerializer(data=request.data)
				if serializer.is_valid():
						serializer.save()
						name1=serializer.data['plantimage1'][1::]
						name2=serializer.data['plantimage2'][1::]
						name3=serializer.data['plantimage3'][1::]
						mp_drawing = mp.solutions.drawing_utils
						mp_hands = mp.solutions.hands
						mp_holistic = mp.solutions.holistic
						mp_holistic.POSE_CONNECTIONS
						b=[]
						c=[]
						d=[]
						with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
								img1 = Image.open(name1) 
								img2 = Image.open(name2) 
								img3 = Image.open(name3) 
								numpydata1 = asarray(img1)
								numpydata2 = asarray(img2)
								numpydata3 = asarray(img3)
								image1 = cv2.cvtColor(numpydata1,cv2.COLOR_BGR2RGB)
								image2 = cv2.cvtColor(numpydata2,cv2.COLOR_BGR2RGB)
								image3 = cv2.cvtColor(numpydata3,cv2.COLOR_BGR2RGB)
								results1 = holistic.process(image1)
								results2 = holistic.process(image2)
								results3 = holistic.process(image3)
								if(len(results1.pose_world_landmarks.landmark)==0 or len(results2.pose_world_landmarks.landmark)==0 or len(results3.pose_world_landmarks.landmark)==0):
									return JsonResponse({"reason":"upload again"}, status=status.HTTP_400_BAD_REQUES)

								else:
									for i in results1.pose_world_landmarks.landmark:
										b.append(i.x)
										c.append(i.y)
										d.append(i.z)

									for i,j in enumerate(results2.pose_world_landmarks.landmark):
										b[i]+=j.x
										c[i]+=j.y
										d[i]+=j.z

									for i,j in enumerate(results3.pose_world_landmarks.landmark):
										b[i]+=j.x
										c[i]+=j.y
										d[i]+=j.z

									for i in range(len(b)):
										b[i]=b[i]/3
										c[i]=c[i]/3
										d[i]=d[i]/3


									s832=distance(b[8], c[8],d[8],b[32], c[32],b[32]) 
									s1331=distance(b[13], c[13],d[13],b[31], c[31],d[31])  
									s2324=distance(b[23], c[23],d[23],b[24], c[24],d[24])  
									s2632=distance(b[26], c[26],d[26],b[32], c[32],d[32])  
									s2331=distance(b[23], c[23],d[23],b[31], c[31],d[31])  
									s1317=distance(b[13], c[13],d[13],b[17], c[17],d[17])  
									s1519=distance(b[15], c[15],d[15],b[19], c[19],d[19])  
									s1315=0.85*distance(b[13], c[13],d[13],b[15], c[15],d[15])   
									s113115=distance(b[11],c[11],d[11],b[31],c[31],d[31])  - distance(b[11],c[11],d[11],b[15],c[15],d[15]) 

									e=[s832,s1331,s2324,s2632,s2331,s1317,s1519,s1315,s113115]


									
									return JsonResponse({"measures":e}, status=status.HTTP_201_CREATED)




					
				else:
						return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def del_images(request):
	for file in os.listdir('./images'):
		if (file.endswith('.png') or file.endswith('.jpeg')):
			os.remove('./images/'+file)

	return JsonResponse({"deleted":True})

