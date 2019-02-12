from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class uploaded_software(models.Model):
	software_name = models.CharField(max_length=200)
	software_location = models.FileField(upload_to='software/')

	def __str__(self):
		return self.software_name

class temp_linux_db(models.Model):
	host_name = models.CharField(max_length=200)
	host_ip =  models.CharField(max_length=200)

	def __str__(self):
		return self.host_name
