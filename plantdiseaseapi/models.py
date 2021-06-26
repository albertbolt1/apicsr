from django.db import models

# Create your models here.
class PlantDiseaseImage(models.Model): 
	plantimage1 = models.ImageField(upload_to='images/')
	plantimage2 = models.ImageField(upload_to='images/')
	plantimage3 = models.ImageField(upload_to='images/')