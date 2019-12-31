from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from main.models import MyUser
from site_panel.models import *
# scheduler = BackgroundScheduler()
# # scheduler.add_jobstore(DjangoJobStore(), "default")
#
#
#
# @register_job(scheduler, "interval", seconds=10)
# def add_presenter_phone_number():
# 	users = MyUser.objects.all()
# 	for user in users:
# 		if user.presenter_id != '':
# 			try:
# 				de = Presenter.objects.get(id=user.presenter_id)
# 				user.phone_number = de.phone_number
# 				user.national_number = de.national_number
# 				user.save()
# 				print('presenter done!')
# 			except:
# 				pass
#
# 		if user.buyer_id != '':
# 			try:
# 				de = Buyer.objects.get(id=user.buyer_id)
# 				user.phone_number = de.phone_number
# 				user.national_number = de.national_number
# 				user.save()
# 				print('buyer done!')
#
# 			except:
# 				pass
#
# 		if user.deceased_id != '':
# 			try:
# 				de = Deceased.objects.get(id=user.deceased_id)
# 				user.national_number = de.national_number
# 				user.save()
# 				print('deceased done!')
#
# 			except:
# 				pass
# 	scheduler.pause()
#
#
#
# register_events(scheduler)
#
#
# amir = BackgroundScheduler()
# # amir.add_jobstore(DjangoJobStore(),"default")
#
# @register_job(amir,'interval',seconds=5)
# def he():
# 	users = MyUser.objects.all()
# 	for user in users:
# 		user.phone_number = None
# 		user.national_number = None
# 		user.save()
# 	print('all done!')
#
# register_events(amir)