from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from .models import *
from datetime import datetime

from django.shortcuts import get_object_or_404

from jdatetime import JalaliToGregorian, GregorianToJalali

from django.contrib.auth.models import Group

from seen.models import *

import random
from django.contrib.auth.decorators import user_passes_test

from django.db.models import Q



def check_superuser(user):
	return user.is_superuser




@user_passes_test(check_superuser)
def Seens(request):
	seens = Counter_Seen.objects.all()
	date = datetime.now().date()
	context = {
		'date':date,
		'seens':seens
	}
	return render(request,'admin-panel/superuser/seen-list.html',context)

@user_passes_test(check_superuser)
def All_Seens(request):
	# return HttpResponse('sasa')
	last_seens = Last_Seen.objects.all()
	context = {
		'seens':last_seens
	}
	return render(request,'admin-panel/superuser/last_seens.html',context)


@user_passes_test(check_superuser)
def Employee_List(request):
	employees = MyUser.objects.filter(is_staff=True)
	context = {
		'employees':employees
	}
	return render(request,'admin-panel/superuser/employee_list.html',context)

@user_passes_test(check_superuser)
def Edit_Employee_Profile(request,id):
	select_employee = MyUser.objects.get(id = id)


	if request.method == 'POST' and 'first_name' in request.POST:
		first_name = request.POST['first_name']
		# return HttpResponse(first_name)
		last_name = request.POST['last_name']
		email = request.POST['email']
		phone_number = request.POST['phone_number']
		national_number = request.POST['national_number']
		username = request.POST['username']
		try:
			user = MyUser.objects.get(username=username)
			if user != select_employee:
				message = 'کاربر با username : {} وجود دارد.'.format(username)
				context = {
					'select_employee':select_employee,
					'error':True,
					'message':message,
					'infor':True,
				}
				return render(request, 'admin-panel/superuser/edit_employee_profile.html', context)
			select_employee.username = username

		except:
			select_employee.username = username
		try:
			select_employee.email = email
			select_employee.phone_number = phone_number
			select_employee.national_number = national_number
			select_employee.first_name = first_name
			select_employee.last_name = last_name

			try:
				picture = request.FILES['picture']
				select_employee.picture = picture
				select_employee.save()
			except:
				pass
			select_employee.save()

			context = {
				'select_employee':select_employee,
				'success': True,
				'infor': True,
				'message': 'مشخصات با موفقیت تغییر یافت.',
			}
			return render(request, 'admin-panel/superuser/edit_employee_profile.html', context)

		except:
			context = {
				'select_employee':select_employee,
				'error': True,
				'infor': True,
				'message': 'مشخصات وارد شده ایراد دارد',
			}
			return render(request, 'admin-panel/superuser/edit_employee_profile.html', context)

	if request.method == 'POST' and 'password' in request.POST:
		password = request.POST['password']
		re_password = request.POST['re_password']


		if password == re_password:
			select_employee.set_password(password)
			select_employee.save()
			context = {
				'success': True,
				'pass_change': True,
				'message': 'تغییر رمز با موفقیت انجام شد.',

			}
			return render(request, 'admin-panel/superuser/edit_employee_profile.html', context)
		else:
			context = {
				'error': True,
				'pass_change': True,
				'message': 'لطفا رمز جدید را با دقت وارد کنید.',
			}
			return render(request, 'admin-panel/profile/profile.html', context)

	context = {
		'select_employee':select_employee
	}
	return render(request,'admin-panel/superuser/edit_employee_profile.html',context)