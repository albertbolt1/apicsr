from rest_framework import serializers 

from .models import PlantDiseaseImage 

class PlantDiseaseImageSerializer(serializers.ModelSerializer): 
	class Meta:
		model=PlantDiseaseImage
		fields=['plantimage1','plantimage2','plantimage3']