from django.urls import path,include
from . import views
from django.conf.urls import url 

urlpatterns = [
	url(r'^upload$', views.MyImageView.as_view(), name='image-upload'),
]
