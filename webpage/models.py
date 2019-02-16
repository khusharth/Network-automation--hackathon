from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class temp_linux_db(models.Model):
	host_name = models.CharField(max_length=200)
	host_ip =  models.CharField(max_length=200)

	def __str__(self):
		return self.host_name


class linux_software(models.Model):
	linux_software_name = models.CharField(max_length=200)
	linux_software_location = models.FileField(upload_to='linux_software/')

	def __str__(self):
		return self.linux_software_name


class playbook(models.Model):
	playbook_name = models.CharField(max_length=200)
	playbook_content = models.TextField(max_length=99999)

	def __str__(self):
		return self.playbook_name
