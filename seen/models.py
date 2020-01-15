from django.db import models

from main.models import *

import socket
# Create your models here.

class Counter_Seen(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=64)
	path = models.URLField()
	user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True)
	counter = models.CharField(max_length=64,default=0)
	computer_info = models.CharField(max_length=508,null=True,blank=True)


	def save(self, *args, **kwargs):


		try:
			host_name = socket.gethostname()
			host_ip = socket.gethostbyname(host_name)
			self.computer_info = host_name + ' ' + host_ip
			super(Counter_Seen,self).save(*args,**kwargs)
		except:
			super(Counter_Seen, self).save(*args, **kwargs)




	def __str__(self):
		if self.user_id:
			return self.user_id.get_full_name() + ' ' + self.counter
		else:
			return self.counter



#
# @receiver(post_save,sender=Counter_Seen)
# def Add(sender, instance, created, *args, **kwargs):
# 	if created:
# 		seen = C