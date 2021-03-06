from django.db import models

from main.models import *

from django.db.models.signals import post_save, pre_save, m2m_changed, pre_delete
from django.dispatch import receiver

from django.shortcuts import render, HttpResponse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


from django.contrib.auth.models import Group


import random

# Create your models here.
class Presenter(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	first_name = models.CharField(max_length=64, verbose_name='نام ')
	last_name = models.CharField(max_length=64, verbose_name='نام خانوادگی ')
	national_number = models.CharField(max_length=11, unique=True, verbose_name='شماره ملی ')
	identification_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره شناسنامه ')
	phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره تماس ')
	address = models.TextField(null=True,blank=True,verbose_name='آدرس معرف ')
	user_id = models.ForeignKey(MyUser,related_name='presenter', on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر ')

	class Meta:
		verbose_name = 'معرف'
		verbose_name_plural = 'معرف'

	def get_full_name(self):
		return self.first_name + ' ' + self.last_name

	def __str__(self):
		return self.get_full_name()


class Place(models.Model):
	STATUS_CHOICES = (
		('Pre_sell', 'پیش فروش شده'),
		('Municipal', 'شهرداری'),
		('Sold', 'فروخته شده')
	)

	TYPE_CHOICES = (
		('Normal', 'عادی'),
		('Celebrities', 'مشاهیر')
	)

	FLOOR_CHOICES = (
		('OneFloor', 'طبقه یک'),
		('TwoFloor', 'طبقه دو')
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	code = models.CharField(max_length=11, null=True, blank=True, unique=True, verbose_name='کد قبر ')
	longitude = models.CharField(max_length=255, verbose_name='طول جغرافیایی ')
	latitude = models.CharField(max_length=255, verbose_name='عرض جغرافیایی ')
	price = models.CharField(max_length=8, default=0, null=True, blank=True, verbose_name='قیمت ')
	ghete = models.CharField(default='', null=True, blank=True, max_length=4, verbose_name='قطعه ')
	radif = models.CharField(max_length=11, verbose_name='ردیف ')
	block = models.CharField(max_length=11, verbose_name='بلوک ')
	number = models.CharField(max_length=11, verbose_name='شماره ')
	floor = models.CharField(max_length=12, choices=FLOOR_CHOICES, default='OneFloor', verbose_name='طبقه ')
	status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Municipal', verbose_name='وضعیت قبر ')
	type = models.CharField(max_length=32, choices=TYPE_CHOICES, default='normal', verbose_name='نوع قبر ')

	class Meta:
		verbose_name = 'قبرها'
		verbose_name_plural = 'قبرها'
		unique_together = [['code', 'ghete', 'radif', 'block', 'number', 'floor'],
						   ['ghete', 'radif', 'block', 'number', 'floor']]

	def __str__(self):
		return str(self.code)


class Deceased(models.Model):
	STATUS_CHOICES = (
		('One', 'one'),
		('Two', 'two'),
	)

	TYPE_CHOICES = (
		('One', 'one'),
		('Two', 'two'),

	)

	SEX_CHOICES = (
		('MALE', 'مرد'),
		('FEMALE', 'زن'),
		('UNKNOWN', 'ناشناخته')
	)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	muni_code = models.IntegerField(null=True,blank=True, verbose_name='شماره ثبت آرامستان ')
	deceased_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='_', verbose_name='وضعیت جنازه ')
	first_name = models.CharField(max_length=64, verbose_name='نام ')
	last_name = models.CharField(max_length=64, verbose_name='نام خانوادگی ')
	national_number = models.CharField(null=True,blank=True,max_length=10, verbose_name='شماره ملی ')
	date_of_birth = models.DateField(verbose_name='تاریخ تولد ')
	sex = models.CharField(max_length=32, choices=SEX_CHOICES, default='UNKNOWN', verbose_name='جنسیت ')
	fa_name = models.CharField(max_length=64, verbose_name='نام پدر ')
	bio = models.TextField(blank=True, null=True, verbose_name='زندگی نامه ')
	mo_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='نام مادر ')
	identification_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره شناسنامه ')
	issue_date = models.DateField(null=True, blank=True, verbose_name='تاریخ صدور ')
	place_of_birth = models.CharField(max_length=32, null=True, blank=True, verbose_name='محل تولد ')
	address = models.TextField(null=True, blank=True, verbose_name='آدرس ')
	presenter_id = models.ForeignKey(Presenter, null=True, blank=True, on_delete=models.CASCADE,
									 verbose_name='معرف ')

	class Meta:
		verbose_name = 'افراد فوت شده'
		verbose_name_plural = 'افراد فوت شده'

	def get_full_name(self):
		return self.first_name + ' ' + self.last_name

	def __str__(self):
		return self.get_full_name()


class Cause_Death(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=128,unique=True,verbose_name='عنوان ')

	class Meta:
		verbose_name = 'علت فوت'
		verbose_name_plural = 'علت فوت'

	def __str__(self):
		return self.name


class Death_Certificate(models.Model):
	STATUS_CHOICE = (
		('Accepted', 'تایید شده'),
		('UnAccepted', 'در انتظار تایید'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	place = models.CharField(max_length=128,null=True,blank=True, verbose_name='محل فوت ')
	doctor_first_name = models.CharField(max_length=64, verbose_name='نام پزشک ')
	doctor_last_name = models.CharField(max_length=64, verbose_name='نام خانوادگی پزشک ')
	medical_system_number = models.CharField(max_length=32, verbose_name='شماره نظام پزشکی ')
	death_certificate_number = models.CharField(max_length=32, verbose_name='شماره گواهی فوت ')
	cause_death_id = models.ForeignKey(Cause_Death,null=True,blank=True,on_delete=models.CASCADE,related_name='cause',verbose_name='علت فوت ')
	date_of_death = models.DateField(null=True, blank=True, verbose_name='تاریخ فوت ')
	deceased_id = models.ForeignKey(Deceased, on_delete=models.CASCADE, related_name='certificate', unique=True,
									verbose_name='متوفی ')
	status = models.CharField(max_length=32, choices=STATUS_CHOICE, default='UnAccepted', verbose_name='تاییدیه ')

	class Meta:
		verbose_name = 'گواهی فوت'
		verbose_name_plural = 'گواهی فوت'

	def __str__(self):
		return self.deceased_id.get_full_name()

	def doctor(self):
		return self.doctor_first_name + ' ' + self.doctor_last_name

	def deceased_national_number(self):
		return self.deceased_id.national_number



class Buyer(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	first_name = models.CharField(max_length=64, verbose_name='نام ')
	last_name = models.CharField(max_length=64, verbose_name='نام خانوادگی ')
	national_number = models.CharField(max_length=11, unique=True, verbose_name='شماره ملی ')
	identification_number = models.CharField(max_length=11, null=True, blank=True, verbose_name='شماره شناسنامه ')
	phone_number = models.CharField(max_length=11,null=True,blank=True, unique=True, verbose_name='شماره تماس ')
	user_id = models.ForeignKey(MyUser,related_name='buyer', on_delete=models.CASCADE, blank=True, null=True, verbose_name='کاربر ')

	class Meta:
		verbose_name = 'خریدار'
		verbose_name_plural = 'خریدار'

	def get_full_name(self):
		return self.first_name + ' ' + self.last_name

	def __str__(self):
		return self.get_full_name()


class Madah(models.Model):
	GRADE_CHOOSE = (
		('Number One', 'درجه یک'),
		('Number Two', 'درجه دو'),
		('Number Three', 'درجه سه'),

	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=64, verbose_name='نام و نام خانوادگی مداح ')
	phone_number = models.CharField(max_length=11, verbose_name='شماره تماس ')
	grade = models.CharField(max_length=64, choices=GRADE_CHOOSE, default=None, verbose_name='سطح ')
	price = models.IntegerField(verbose_name='هزینه ')

	class Meta:
		verbose_name = 'مداحان'
		verbose_name_plural = 'مداحان'

	def __str__(self):
		return self.name + self.grade


class Reader_Service(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	start_time = models.DateTimeField(verbose_name='زمان شروع ')
	madah_id = models.ForeignKey(Madah, related_name='reader', on_delete=models.CASCADE, blank=True, null=True,
								 verbose_name='مداح ')
	deceased_id = models.ForeignKey(Deceased, on_delete=models.CASCADE, verbose_name='متوفی ')
	user_id = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='سفارش دهنده ')
	total_price = models.IntegerField(default=0, verbose_name='هزینه ')

	class Meta:
		verbose_name = 'خدمات مداحان'
		verbose_name_plural = 'خدمات مداحان'

	def __str__(self):
		return self.user_id.user_id.get_full_name() + ' ' + self.deceased_id.first_name + ' ' + self.deceased_id.last_name

	def save(self, *args, **kwargs):
		self.total_price = self.madah_id.price
		super(Reader_Service, self).save(*args, **kwargs)


class Marasem(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	name = models.CharField(max_length=64, verbose_name='نام ')
	big_table = models.IntegerField(verbose_name='میز بزرگ ')
	echo = models.IntegerField(verbose_name='اکو ')
	panel = models.IntegerField(verbose_name='تابلو ')
	tent = models.IntegerField(verbose_name='چادر با پرده دو طرفه ')
	chair = models.IntegerField(verbose_name='صندلی ')
	carpet = models.IntegerField(verbose_name='فرش ')
	eating_table = models.IntegerField(verbose_name='میز غذا خوری ')
	price = models.IntegerField(verbose_name='هزینه ')

	class Meta:
		verbose_name = 'مجالس'
		verbose_name_plural = 'مجالس'

	def __str__(self):
		return self.name


class Memorial_Service(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	start_time = models.DateTimeField(verbose_name='زمان شروع ')
	marasem_id = models.ForeignKey(Marasem, related_name='memorial', on_delete=models.CASCADE, blank=True, null=True,
								   verbose_name='مجلس ')
	deceased_id = models.ForeignKey(Deceased, on_delete=models.CASCADE, verbose_name='متوفی ')
	user_id = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='سفارش دهنده ')
	total_price = models.IntegerField(default=0, verbose_name='کل هزینه ')

	class Meta:
		verbose_name = 'خدمات مجالس'
		verbose_name_plural = 'خدمات مجالس'

	def __str__(self):
		return self.user_id.user_id.get_full_name() + ' ' + self.deceased_id.first_name + ' ' + self.deceased_id.last_name

	def save(self, *args, **kwargs):
		self.total_price = self.marasem_id.price
		super(Memorial_Service, self).save(*args, **kwargs)


class Place_Service(models.Model):
	PAYMENT_STATUS = (
		('NOT_PAID', 'تسویه نشده'),
		('PAID', 'تسویه شد')
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	buyer_id = models.ForeignKey(Buyer,null=True,blank=True, on_delete=models.CASCADE, verbose_name='خریدار ')
	place_id = models.OneToOneField(Place, related_name='place_service', on_delete=models.CASCADE, verbose_name='قبر ')
	deceased_id = models.ForeignKey(Deceased, on_delete=models.CASCADE, null=True, blank=True,
									verbose_name='متوفی مربوطه ')
	document = models.CharField(max_length=32, blank=True, null=True, verbose_name='شماره سند ')
	payment_status = models.CharField(max_length=32, choices=PAYMENT_STATUS, default='NOT_PAID',
									  verbose_name='وضعیت پرداخت ')

	class Meta:
		verbose_name = 'سفارش قبر'
		verbose_name_plural = 'سفارش قبر'



	def __str__(self):
		return self.payment_status + ' ' + str(
			self.place_id.code) + ' ' + self.place_id.status


class Option(models.Model):
	name = models.CharField(max_length=64, verbose_name='نام ')
	price = models.IntegerField(verbose_name='هزینه ')

	class Meta:
		verbose_name = 'امکانات'
		verbose_name_plural = 'امکانات'

	def __str__(self):
		return self.name


class After_Death_Service(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	start_time = models.DateTimeField(verbose_name='زمان شروع ')
	option_id = models.ManyToManyField(Option, related_name='option', blank=True, null=True, verbose_name='امکانات ')
	deceased_id = models.ForeignKey(Deceased, on_delete=models.CASCADE, verbose_name='متوفی ')
	user_id = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name='سفارش دهنده ')
	total_price = models.IntegerField(default=0, verbose_name='کل هزینه ')

	class Meta:
		verbose_name = 'خدمات پس از مرگ'
		verbose_name_plural = 'خدمات پس از مرگ'

	def __str__(self):
		return self.user_id.user_id.get_full_name() + ' ' + self.deceased_id.first_name + ' ' + self.deceased_id.last_name


class Service_List(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	code = models.IntegerField(unique=True,null=True,blank=True)
	name = models.CharField(max_length=64, verbose_name='نام خدمات ')
	price = models.CharField(max_length=8, verbose_name='هزینه ')

	class Meta:
		verbose_name = 'لیست خدمات'
		verbose_name_plural = 'لیست خدمات'

	def __str__(self):
		return self.name + ' ' + self.price

class Additional_Service(models.Model):
	STATUS = (
		('PAID', 'پرداخت شده'),
		('NOT PAID', 'پرداخت نشده'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	service_id = models.ForeignKey(Service_List,on_delete=models.CASCADE,null=True,blank=True,verbose_name='خدمات مربوطه ')
	buyer_id = models.ForeignKey(Buyer,related_name='additional', null=True, blank=True, on_delete=models.CASCADE, verbose_name='خریدار ')
	status = models.CharField(max_length=32, choices=STATUS, default='NOT PAID', verbose_name='وضعیت پرداخت ')
	deceased_id = models.ForeignKey(Deceased, related_name='additional_service', on_delete=models.CASCADE,
									verbose_name='متوفی ')

	class Meta:
		verbose_name = 'خدمات اضافه'
		verbose_name_plural = 'خدمات اضافه'

	def __str__(self):
		return self.deceased_id.get_full_name() + ' ' + self.service_id.name


class Target(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	code = models.CharField(max_length=8,unique=True, null=True, blank=True)
	name = models.CharField(max_length=64, verbose_name='مقصد ')
	price = models.CharField(max_length=8, verbose_name='هزینه ')

	class Meta:
		verbose_name = 'مقصد حمل و نقل'
		verbose_name_plural = 'مقصد حمل و نقل'

	def __str__(self):
		return self.name

class Driver(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	user_id = models.ForeignKey(MyUser,on_delete=models.CASCADE,null=True,blank=True,verbose_name='کاربر مربوطه ')
	code = models.CharField(max_length=64,null=True,blank=True,verbose_name='کد راننده ')
	first_name = models.CharField(max_length=255,null=True,blank=True,verbose_name='نام ')
	last_name = models.CharField(max_length=255,null=True,blank=True,verbose_name='نام خانوادگی ')
	national_number = models.CharField(max_length=10,null=True,blank=True,verbose_name='شماره ملی ')
	phone_number = models.CharField(max_length=11,null=True,blank=True,verbose_name='شماره تماس ')

	class Meta:
		verbose_name = 'راننده'
		verbose_name_plural = 'راننده'

	def __str__(self):
		return self.user_id.get_full_name()

class Car(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	code = models.CharField(max_length=32,null=True,blank=True,verbose_name='کد ماشین ')

	class Meta:
		verbose_name = 'ماشین ها'
		verbose_name_plural = 'ماشین ها'

	def __str__(self):
		return self.code

class Movement_Service(models.Model):
	STATUS = (
		('confirmation', 'تایید شده'),
		('disapproval', 'در حال بررسی'),
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	start_date = models.DateField(null=True, blank=True, verbose_name='تاریخ شروع ')
	start_time = models.TimeField(null=True, blank=True, verbose_name='زمان شروع ')
	target_id = models.ForeignKey(Target, on_delete=models.CASCADE, null=True, blank=True,verbose_name='مقصد مربوطه ')
	price = models.CharField(max_length=32,null=True,blank=True,verbose_name='قیمت ')
	car_id = models.ForeignKey(Car, related_name='movement_service', null=True, blank=True, on_delete=models.CASCADE,verbose_name='ماشین مربوطه ')
	status = models.CharField(max_length=32, choices=STATUS, default='NOT PAID', verbose_name='وضعیت پرداخت ')
	driver_id = models.ForeignKey(Driver,on_delete=models.CASCADE,null=True,blank=True, verbose_name='راننده ')
	deceased_id = models.ForeignKey(Deceased, on_delete=models.CASCADE,verbose_name='متوفی ')
	buyer_id = models.ForeignKey(Buyer, on_delete=models.CASCADE,verbose_name='معرف ')


	class Meta:
		verbose_name = 'حمل متوفی'
		verbose_name_plural = 'حمل متوفی'

	def __str__(self):
		return self.deceased_id.get_full_name()


class Bill(models.Model):
	STATUS = (
		('PAID','پرداخت شده'),
		('NOT PAID','پرداخت نشده'),
	)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	code = models.CharField(max_length=32,null=True,blank=True)
	document = models.CharField(max_length=32,null=True,blank=True)
	name = models.CharField(max_length=64, verbose_name='عنوان ')
	price = models.CharField(max_length=8, verbose_name='هزینه ')
	order_id = models.ForeignKey(Place_Service, on_delete=models.CASCADE, null=True, blank=True,
								 verbose_name='قبر مربوطه ')
	after_death_service_id = models.ForeignKey(After_Death_Service, on_delete=models.CASCADE, null=True, blank=True,
											   verbose_name='خدمات پس از مرگ مربوطه ')
	memorial_service_id = models.ForeignKey(Memorial_Service, on_delete=models.CASCADE, null=True, blank=True,
											verbose_name='جلسه مربوطه ')
	reader_service_id = models.ForeignKey(Reader_Service, on_delete=models.CASCADE, null=True, blank=True,
										  verbose_name='مداح مربوطه ')
	deceased_id = models.ForeignKey(Deceased, on_delete=models.CASCADE, null=True, blank=True, verbose_name='متوفی ')
	additional_service_id = models.ForeignKey(Additional_Service, on_delete=models.CASCADE, null=True, blank=True,
											  verbose_name='خدمات اضافه مربوطه ')

	movement_service_id = models.ForeignKey(Movement_Service,related_name='bill', on_delete=models.CASCADE, null=True, blank=True,
											  verbose_name='حمل و نقل مربوطه ')

	user_id = models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True, verbose_name='خرید توسط ')
	status = models.CharField(max_length=64,default='NOT PAID',choices=STATUS,verbose_name='وضعیت پرداخت ')

	class Meta:
		verbose_name = 'کلیه خریدها'
		verbose_name_plural = 'کلیه خریدها'

	def __str__(self):
		return self.name +' '+self.price


class License(models.Model):
	LICENSE_STATUS = (
		('WAITING', 'درحال بررسی'),
		('CONFIRMED', 'تایید شده')
	)

	MOVE_STATUS = (
		('SEND-OUT', 'اعزامی'),
		('FERDOS-REZA', 'فردوس رضا'),
	)

	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	document = models.CharField(max_length=32, unique=True, verbose_name='شماره مجوز ')
	place_id = models.ForeignKey(Place, related_name='license', null=True, blank=True, on_delete=models.CASCADE,
								 verbose_name='قبر مربوطه ')
	deceased_id = models.ForeignKey(Deceased, related_name='license', on_delete=models.CASCADE, verbose_name='متوفی ')
	license_status = models.CharField(max_length=32, choices=LICENSE_STATUS, default='WAITING',
									  verbose_name='وضعیت مجوز ')
	move_status = models.CharField(max_length=32, choices=MOVE_STATUS, default='FERDOS-REZA',
								   verbose_name='وضعیت انتقال ')
	city_name = models.CharField(max_length=32, null=True, blank=True, verbose_name='شهر اعزامی ')

	class Meta:
		verbose_name = 'مجوز دفن'
		verbose_name_plural = 'مجوز دفن'

	def __str__(self):
		return self.deceased_id.get_full_name()

	def deceased_national_number(self):
		return self.deceased_id.national_number


class Grave_Stone(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	buyer_id = models.ForeignKey(Buyer,on_delete=models.CASCADE)
	deceased_id = models.ForeignKey(Deceased,on_delete=models.CASCADE)

	def __str__(self):
		return self.buyer_id.get_full_name()

class Document(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	description = models.TextField(verbose_name='توضیحات ')
	picture = models.ImageField(upload_to='documents/',verbose_name='تصویر ')
	deceased_id = models.ForeignKey(Deceased,on_delete=models.CASCADE,null=True,blank=True,verbose_name='متوفی مربوطه ')

	class Meta:
		verbose_name = 'اسناد'
		verbose_name_plural = 'اسناد'

	def __str__(self):
		if self.deceased_id:
			return self.deceased_id.get_full_name()
		else:
			return str(self.id)

class Archive(models.Model):
	STATUS = (
		('Inbox','دریافتی'),
		('Send','ارسالی')
	)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	code = models.CharField(max_length=32,unique=True,verbose_name='کد ')
	description = RichTextUploadingField(verbose_name='توضیحات ')
	picture = models.ImageField(null=True,blank=True,verbose_name='تصویر ')
	status = models.CharField(max_length=32,choices=STATUS,default='Send',verbose_name='وضعیت ')

	class Meta:
		unique_together = [['code','status']]
		verbose_name_plural = 'بایگانی'
		verbose_name = 'بایگانی'

	def __str__(self):
		return self.code + ' ' + self.status

#
# class Movement_Certificate(models.Model):
# 	STATUS = (
# 		('confirmation', 'تایید'),
# 		('disapproval', 'عدم تایید')
# 	)
# 	created = models.DateTimeField(auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True)
# 	license_id = models.ForeignKey(License,on_delete=models.CASCADE)
# 	status = models.CharField(max_length=32,choices=STATUS,default='disapproval',verbose_name='وضعیت ')
# 	start_date = models.DateField(null=True, blank=True, verbose_name='تاریخ شروع ')
# 	start_time = models.TimeField(null=True, blank=True, verbose_name='زمان شروع ')
# 	driver_id = models.ForeignKey(Driver,null=True,blank=True, on_delete=models.CASCADE, verbose_name='راننده مربوطه ')
# 	car_id = models.ForeignKey(Car,on_delete=models.CASCADE,null=True,blank=True,verbose_name='ماشین مورد نظر ')
# 	description = models.TextField(null=True, blank=True, verbose_name='توضیحات ')
#
# 	class Meta:
# 		verbose_name = 'مجوز حمل'
# 		verbose_name_plural = 'مجوز حمل'
#
# 	def __str__(self):
# 		return self.status + ' ' + self.license_id.deceased_id.get_full_name()



@receiver(post_save,sender=Driver)
def AddToUser(sender, instance, created, *args, **kwargs):
	try:
		driver_group = Group.objects.get(name='driver')
	except:
		driver_group = Group.objects.create(name='driver')
	if created:
		try:
			user = MyUser.objects.get(username=instance.national_number)
			user.driver_id = instance.id
			driver_group.user_set.add(user)
			driver_group.save()
			user.save()
			driver = instance
			driver.user_id = user
			driver.save()
		except:
			MyUser.objects.create(first_name=instance.first_name, last_name=instance.last_name,
								  driver_id=instance.id,national_number=instance.national_number,phone_number=instance.phone_number,
								  email=instance.national_number + '@gmail.com', username=instance.national_number)
			user = MyUser.objects.get(first_name=instance.first_name, last_name=instance.last_name,
									  driver_id=instance.id,
									  email=instance.national_number + '@gmail.com', username=instance.national_number)
			driver_group.user_set.add(user)
			driver_group.save()
			user.set_password(instance.national_number)
			user.save()
			driver = instance
			driver.user_id = user
			driver.save()
	else:

		user = MyUser.objects.get(driver_id=instance.id)
		user.first_name = instance.first_name
		user.last_name = instance.last_name
		user.email = instance.national_number
		user.username = instance.national_number
		user.set_password(instance.national_number)
		user.save()






@receiver(post_save, sender=Additional_Service)
def AddToBill(sender, instance, created, *args, **kwargs):
	if created and instance.status == 'PAID':
		bill = Bill.objects.create(code=instance.service_id.code,name=instance.service_id.name, price=instance.service_id.price, additional_service_id=instance,
								   deceased_id=instance.deceased_id, user_id=instance.buyer_id,status='PAID')
	else:
		if instance.status == 'PAID':
			try:
				bill = Bill.objects.get(additional_service_id=instance, deceased_id=instance.deceased_id)
				bill.price = instance.service_id.price
				bill.buyer_id = instance.buyer_id
				bill.status = 'PAID'
				bill.code = instance.service_id.code
				bill.save()
			except:
				bill = Bill.objects.create(code=instance.service_id.code,name=instance.service_id.name, price=instance.service_id.price, additional_service_id=instance,
										   deceased_id=instance.deceased_id, user_id=instance.buyer_id,document=RandForBill(),status='PAID')
		else:
			try:
				bill = Bill.objects.get(additional_service_id=instance)
				bill.delete()
			except:
				pass



@receiver(post_save, sender=Movement_Service)
def AddMovementToBill(sender, instance, created, *args, **kwargs):
	if created :
		bill = Bill.objects.create(code=instance.target_id.code,name=instance.target_id.name, price=instance.target_id.price, movement_service_id=instance,
								   deceased_id=instance.deceased_id, user_id=instance.buyer_id,status='PAID')
	else:
			try:
				bill = Bill.objects.get(movement_service_id=instance, deceased_id=instance.deceased_id)
				bill.price = instance.target_id.price
				bill.buyer_id = instance.buyer_id
				bill.code = instance.target_id.code
				bill.save()
			except:
				bill = Bill.objects.create(code=instance.target_id.code,name=instance.target_id.name, price=instance.target_id.price, movement_service_id=instance,
								   deceased_id=instance.deceased_id, user_id=instance.buyer_id,status='PAID')



def RandForDocument():
	while(True):
		number = random.randint(100000,999999)

		try:
			license = License.objects.get(document=number)
		except:
			return number

#
# @receiver(post_save, sender=License)
# def AddMovmentCertificate(sender, instance, created, *args, **kwargs):
# 	if created:
# 		if instance.move_status == 'SEND-OUT':
# 			movement_cer = Movement_Certificate.objects.create(license_id=instance)


@receiver(post_save, sender=Deceased)
def Add_Death_certificate(sender, instance, created, *args, **kwargs):
	deceased = instance
	if created:
		if  deceased.national_number:
			user = None
			try:
				user = MyUser.objects.get(username=instance.national_number)
				user.deceased_id = instance.id
				user.save()
			except:
				MyUser.objects.create(first_name=instance.first_name, last_name=instance.last_name, deceased_id=instance.id,
									  email=instance.national_number + '@gmail.com', username=instance.national_number,national_number=instance.national_number)
				user = MyUser.objects.get(first_name=instance.first_name, last_name=instance.last_name,
										  deceased_id=instance.id,
										  email=instance.national_number + '@gmail.com', username=instance.national_number)
				user.set_password(instance.national_number)
				user.save()

		death_certificate = Death_Certificate.objects.create(deceased_id=deceased)

		license = License.objects.create(deceased_id=deceased, license_status='WAITING',
										 document=RandForDocument())
	else:
		if deceased.national_number:
			try:
				user = MyUser.objects.get(deceased_id=instance.id)
				user.first_name = instance.first_name
				user.last_name = instance.last_name
				user.email = instance.national_number
				user.username = instance.national_number
				user.set_password(instance.national_number)
				user.save()
			except:
				MyUser.objects.create(first_name=instance.first_name, last_name=instance.last_name,
									  deceased_id=instance.id,
									  email=instance.national_number + '@gmail.com', username=instance.national_number)
				user = MyUser.objects.get(first_name=instance.first_name, last_name=instance.last_name,
										  deceased_id=instance.id,
										  email=instance.national_number + '@gmail.com',
										  username=instance.national_number)
				user.set_password(instance.national_number)
				user.save()

@receiver(pre_delete, sender=Deceased)
def Edit_Place(sender, instance, *args, **kwargs):
	try:
		licence = License.objects.get(deceased_id=instance)
		place = licence.place_id
		place.status = 'Municipal'
		place.save()
	except:
		pass


@receiver(post_delete, sender=Deceased)
def DeleteDeceasedFromUser(sender, instance, *args, **kwargs):
	try:
		user = MyUser.objects.get(username=instance.national_number)
		user.deceased_id = None
		user.save()
	except:
		pass


@receiver(post_save, sender=Presenter)
def AddPresenterToUser(sender, instance, created, *args, **kwargs):
	if created:
		try:
			user = MyUser.objects.get(username=instance.national_number)
			user.presenter_id = instance.id
			user.save()
			presenter = instance
			presenter.user_id = user
			presenter.save()
		except:
			MyUser.objects.create(first_name=instance.first_name, last_name=instance.last_name,
								  presenter_id=instance.id,national_number=instance.national_number,phone_number=instance.phone_number,
								  email=instance.national_number + '@gmail.com', username=instance.national_number)
			user = MyUser.objects.get(first_name=instance.first_name, last_name=instance.last_name,
									  presenter_id=instance.id,
									  email=instance.national_number + '@gmail.com', username=instance.national_number)
			user.set_password(instance.national_number)
			user.save()
			presenter = instance
			presenter.user_id = user
			presenter.save()
	else:
		user = MyUser.objects.get(presenter_id=instance.id)
		user.first_name = instance.first_name
		user.last_name = instance.last_name
		user.email = instance.national_number
		user.username = instance.national_number
		user.set_password(instance.national_number)
		user.save()


@receiver(post_delete, sender=Driver )
def DeleteDriverFromUser(sender, instance, *args, **kwargs):
	try:
		user = MyUser.objects.get(username=instance.national_number)
		user.driver_id = None
		user.save()
	except:
		pass

@receiver(post_delete, sender=Presenter)
def DeletePresenterFromUser(sender, instance, *args, **kwargs):
	try:
		user = MyUser.objects.get(username=instance.national_number)
		user.deceased_id = None
		user.save()
	except:
		pass


@receiver(post_delete, sender=Buyer)
def DeleteBuyerFromUser(sender, instance, *args, **kwargs):
	try:
		user = MyUser.objects.get(username=instance.national_number)
		user.buyer_id = None
		user.save()
	except:
		pass


@receiver(m2m_changed, sender=After_Death_Service.option_id.through)
def total_price_computer(sender, instance, action, reverse, pk_set, **kwargs):
	if action == "post_add":
		options = pk_set
		x = instance.total_price
		after = instance
		for option in options:
			o = Option.objects.get(pk=option)
			x = x + o.price
		after.total_price = x
		after.save()

	if action == "post_remove":
		options = pk_set
		x = instance.total_price
		after = instance
		for option in options:
			o = Option.objects.get(pk=option)
			x = x - o.price
		after.total_price = x
		after.save()


@receiver(pre_delete, sender=Place_Service)
def DeleteBillandChangePlaceStatus(sender, instance, *args, **kwargs):
	if instance.payment_status == 'PAID':
		try:
			place = instance.place_id
			place.status = 'Municipal'
			place.save()
			bill = Bill.objects.get(order_id=instance)
			bill.delete()
		except:
			pass


@receiver(post_save, sender=Place_Service)
def AddOrderToBill(sender, instance, created, *args, **kwargs):
	if created and instance.payment_status == 'PAID':
		if instance.deceased_id:
			if instance.buyer_id:
				Bill.objects.create(name='خرید قبر', price=instance.place_id.price, order_id=instance,
									deceased_id=instance.deceased_id, user_id=instance.buyer_id)
				place = instance.place_id
				place.status = 'Sold'
				place.save()
			else:
				Bill.objects.create(name='خرید قبر', price=instance.place_id.price, order_id=instance,
									deceased_id=instance.deceased_id)
				place = instance.place_id
				place.status = 'Sold'
				place.save()
		else:
			Bill.objects.create(name='خرید قبر', price=instance.place_id.price, order_id=instance,
								user_id=instance.buyer_id)
			place = instance.place_id
			place.status = 'Pre_sell'
			place.save()
	else:
		if instance.payment_status == 'PAID':
			if instance.deceased_id:
				try:
					Bill.objects.get(name='خرید قبر', price=instance.place_id.price, order_id=instance,
									 deceased_id=instance.deceased_id, user_id=instance.buyer_id)
				except:
					Bill.objects.create(name='خرید قبر', price=instance.place_id.price, order_id=instance,
										deceased_id=instance.deceased_id, user_id=instance.buyer_id)
					place = instance.place_id
					place.status = 'Sold'
					place.save()
			else:
				try:
					Bill.objects.get(name='خرید قبر', price=instance.place_id.price, order_id=instance,
									 user_id=instance.buyer_id)
				except:
					Bill.objects.create(name='خرید قبر', price=instance.place_id.price, order_id=instance,
										user_id=instance.buyer_id)
					place = instance.place_id
					place.status = 'Pre_sell'
					place.save()


@receiver(post_save, sender=Buyer)
def AddBuyerToUser(sender, instance, created, *args, **kwargs):
	if created:
		try:
			user = MyUser.objects.get(username=instance.national_number)
			user.buyer_id = instance.id
			user.save()
			buyer = instance
			buyer.user_id = user
			buyer.save()
		except:
			MyUser.objects.create(first_name=instance.first_name, last_name=instance.last_name,
								  buyer_id=instance.id,national_number=instance.national_number,phone_number=instance.phone_number,
								  email=instance.national_number + '@gmail.com', username=instance.national_number)
			user = MyUser.objects.get(first_name=instance.first_name, last_name=instance.last_name,
									  buyer_id=instance.id,
									  email=instance.national_number + '@gmail.com', username=instance.national_number)

			user.set_password(instance.national_number)
			user.save()
			buyer = instance
			buyer.user_id = user
			buyer.save()
	else:
		user = MyUser.objects.get(buyer_id=instance.id)
		user.first_name = instance.first_name
		user.last_name = instance.last_name
		user.email = instance.national_number
		user.username = instance.national_number
		user.set_password(instance.national_number)
		user.save()


@receiver(post_save, sender=License)
def EditBuyrDeceased(sender, instance, created, *args, **kwargs):
	license = instance
	national_numer = license.deceased_id.national_number
	self = None
	place_service = None
	try:
		place_service = Place_Service.objects.get(buyer_id__national_number=national_numer)
		self = True
	except:
		self = False
	if self:
		place_service.deceased_id = instance.deceased_id
		place_service.save()

	if instance.place_id:
		place = instance.place_id
		place.status = 'Sold'
		place.save()
	#
	# if instance.move_status == 'SEND-OUT':
	# 	try:
	# 		movement_certificate = Movement_Certificate.objects.get(license_id=instance)
	# 	except:
	# 		movement_certificate = Movement_Certificate.objects.create(license_id=instance, status='disapproval')


@receiver(post_save, sender=Place)
def UpdateBillPlacePrice(sender, instance, created, *args, **kwargs):
	if created:
		pass
	else:
		if instance.price != 0:
			try:
				license = License.objects.get(place_id=instance)
				if license.license_status == 'CONFIRMED':
					try:
						place_service = Place_Service.objects.get(place_id=instance)
						bill = Bill.objects.get(order_id=place_service)
						bill.price = instance.price
						bill.save()
					except:
						place_service = Place_Service.objects.create(place_id=instance, deceased_id=license.deceased_id,
																	 payment_status='PAID')
			except:
				pass



# @receiver(post_save,sender=Order)
# def Add_Order(sender,instance,created,*args,**kwargs):
# 	if created and instance.payment_status == 'PAID' :
# 		conition = None
# 		license =None
# 		try:
# 			license = instance.place_id.license.select_related().get()
# 			conition = True
# 		except:
# 			conition = False
# 		if conition:
# 			# print(instance.place_id.license.deceased_id)
# 			Bill.objects.create(name='خرید قبر',deceased_id=license.deceased_id,price=instance.place_id.price)
# 		else:
# 			Bill.objects.create(name='خرید قبر',price=instance.place_id.price,user = instance.buyer_id)
# 	else:
# 		if instance.payment_status == 'PAID':
# 			conition = None
# 			license = None
#
#
# 			try:
# 				license = instance.place_id.license.select_related().get()
# 				conition = True
# 			except:
# 				conition = False
#
#
#
# 			if conition:
# 				try:
# 					Bill.objects.get(name='خرید قبر',deceased_id=license.deceased_id,price=instance.place_id.price)
# 					deceased = True
# 				except:
# 					deceased =False
#
# 				if deceased:
# 					pass
# 				else:
# 					Bill.objects.create(name='خرید قبر', deceased_id=license.deceased_id, price=instance.place_id.price)
#
#
# 			else:
# 				try:
# 					Bill.objects.get(name='خرید قبر',price=instance.place_id.price,user = instance.buyer_id)
# 					buyer = True
# 				except:
# 					buyer = False
#
# 				if buyer:
# 					pass
# 				else:
# 					Bill.objects.create(name='خرید قبر', price=instance.place_id.price, user=instance.buyer_id)
# else:
# 	if instance.status == 'PAID':
# 		bill = Bill.objects.get()
#


# class Payment_Information(models.Model):
# 	created = models.DateTimeField(auto_now_add=True)
# 	updated = models.DateTimeField(auto_now=True)
# 	deceased_id = models.ForeignKey(Deceased,on_delete=models.CASCADE,verbose_name='متوفی ')
# 	bill_id = models.ManyToManyField(Bill,related_name='payment',verbose_name='خرید های مربوطه ')
# 	total_price = models.CharField(max_length=10,verbose_name='کل هزینه ها ')
# 	class Meta:
# 		verbose_name_plural = ''
# 		verbose_name = 'امور مالی'
