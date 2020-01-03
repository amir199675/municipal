from django.db import models

from django.db.models.signals import post_save ,pre_save , post_delete
from django.dispatch import receiver


# Create your models here.

from django.contrib.auth.models import AbstractUser



class MyUser(AbstractUser):
	deceased_id = models.CharField(max_length=6,null=True,blank=True,editable=False)
	buyer_id = models.CharField(max_length=6,null=True,blank=True,editable=False)
	presenter_id = models.CharField(max_length=6,null=True,blank=True,editable=False)
	driver_id = models.CharField(max_length=6,null=True,blank=True,editable=False)
	national_number = models.CharField(max_length=10,null=True,blank=True,editable=False)
	phone_number = models.CharField(max_length=11,null=True,blank=True)



class New(models.Model):
	STATUS = {
		('Publish','publish'),
		('Draft','draft')
	}
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	title = models.CharField(max_length=128,verbose_name='موضوع ')
	content = models.TextField(verbose_name='محتوا ')
	picture = models.ImageField(upload_to='news-pic/',default='news-pic/default.png',null=True,blank=True ,verbose_name='تصویر ')
	status = models.CharField(max_length=32,choices=STATUS,default='Draft',verbose_name='وضعیت ')
	class Meta:
		verbose_name = 'اخبار'
		verbose_name_plural = 'اخبار'
	def __str__(self):
		return self.title +' '+self.status

class Hadith(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=64,verbose_name='نام شخصیت ')
	content = models.TextField(verbose_name='متن حدیث ')
	picture = models.ImageField(upload_to='Hadith-pic/',verbose_name='تصویر ')
	class Meta:
		verbose_name = 'احادیث'
		verbose_name_plural = 'احادیث'
	def __str__(self):
		return self.name + ' ' + self.content[:50]



class Slider(models.Model):
	STATUS = (
		('Inactive','غیر فعال'),
		('Active','فعال'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	small_text = models.TextField(verbose_name='متن کوچکتر ')
	bold_text = models.TextField(verbose_name='متن بولد ')
	picture = models.ImageField(upload_to='slider-pic/',verbose_name='تصویر ')
	status = models.CharField(max_length=32,choices=STATUS , default='Inactive',verbose_name='وضعیت ')
	class Meta:
		verbose_name = 'اسلایدر'
		verbose_name_plural = 'اسلایدر'
	def __str__(self):
		return self.small_text[:32] + ' - ' + self.bold_text[:32]

class Message(models.Model):
	STATUS = (
		('Read', 'خوانده شد'),
		('UnRead', 'خوانده نشده'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	email = models.EmailField()
	first_name = models.CharField(max_length=128)
	last_name = models.CharField(max_length=128)
	subject = models.CharField(max_length=128)
	content = models.TextField()
	status = models.CharField(max_length=32,choices=STATUS,default='UnRead')

	class Meta:
		verbose_name = 'درخواست ها'
		verbose_name_plural = 'درخواست ها'
	def __str__(self):
		return self.email + self.subject