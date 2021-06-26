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

									e=[b,c,d]

									return JsonResponse({"measures":e}, status=status.HTTP_201_CREATED)



					
				else:
						return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)