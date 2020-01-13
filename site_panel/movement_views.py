from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from .models import *
from django.db.models import Q

from datetime import datetime
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_object_or_404

from jdatetime import JalaliToGregorian, GregorianToJalali

# from  site_panel.tasks import scheduler
# from  site_panel.tasks import amir


def check_staff(user):
	return user.is_staff


def Movement_Lic(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		select_deceased = Deceased.objects.get(id=id)
		buyers = Buyer.objects.all()
		drivers = Driver.objects.all()
		cars = Car.objects.all()
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			buyer_id = request.POST['buyer']
			buyer = None
			if buyer_id == '':
				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				phone_number = request.POST['phone_number']
				national_number = request.POST['national_number']
				try:
					buyer = Buyer.objects.create(first_name=first_name,last_name=last_name,phone_number=phone_number,national_number=national_number)
				except:
					return HttpResponse('خطا در ذخیره سازی اطلاعات معرف')
			else:
				buyer = Buyer.objects.get(id=buyer_id)
			driver = request.POST['driver']
			driver_id = Driver.objects.get(id=driver)
			target = request.POST['target']
			target_id = Target.objects.get(id=target)
			start_date = request.POST['date']
			car = request.POST['car']
			car_id = Car.objects.get(id = car)

			try:
				start_date_miladi = datetime.strptime(start_date, '%Y/%m/%d')
				day = start_date_miladi.day
				year = start_date_miladi.year
				month = start_date_miladi.month
				date = JalaliToGregorian(year, month, day)
				date = date.getGregorianList()
				year = date[0]
				month = date[1]
				day = date[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				date = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				date = None
			start_time = request.POST['time']
			status = request.POST['status']
			try:
				movement_service = Movement_Service.objects.create(start_date=date,start_time=start_time,
																   target_id=target_id,price=target_id.price,car_id=car_id,
																   status=status,driver_id=driver_id,deceased_id=select_deceased,buyer_id=buyer)

			except:
				return HttpResponse('مشکل در ذخیره سازی اطلاعات')

			bill = Bill.objects.get(movement_service_id=movement_service)
			message = 'سرویس حمل و نقل با شماره فاکتور {} با موفقیت توسط {} ثبت شد.'.format(bill.document,bill.user_id.get_full_name())
			buyers = Buyer.objects.all()
			context = {
				'select_deceased':select_deceased,
				'buyers':buyers,
				'success':True,
				'message':message
			}
			return render(request, 'admin-panel/movement/movement_license.html', context)
		targets = Target.objects.all()

		context = {
			'buyers':buyers,
			'cars': cars,
			'targets': targets,
			'select_deceased': select_deceased,
			'drivers': drivers

		}
		return render(request, 'admin-panel/movement/movement_license.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/movement_certificate/{}'.format(id))

@user_passes_test(check_staff)
def Movement_License_List(request,id):
	select_deceased = Deceased.objects.get(id=id)
	services = Movement_Service.objects.filter(deceased_id=select_deceased)
	context = {
		'select_deceased':select_deceased,
		'services':services,


	}
	return render(request,'admin-panel/movement/movement_license_list.html',context)



@user_passes_test(check_staff)
def Add_Target(request):

	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		code = request.POST['code']
		price = request.POST['price']
		name = request.POST['name']
		target = Target.objects.filter(Q(name=name)|Q(code=code))
		if target.count() != 0 :
			context = {
				'error':True,
				'message':'مقصد با اطلاعات وارد شده وجود دارد. لطفا از یکتایی کد و نام مقصد اطمینان حاصل فرمایید'
			}
			return render(request,'admin-panel/movement/add_target.html',context)
		else:
			target = Target.objects.create(name=name,code=code,price=price)
			message = 'مقصد با نام "{}" و کد {} با موفقیت ایجاد شد.'.format(target.name,target.code)
			context = {
				'success':True,
				'message':message
			}
			return render(request,'admin-panel/movement/add_target.html',context)
	context = {

	}
	return render(request,'admin-panel/movement/add_target.html',context)

@user_passes_test(check_staff)
def Target_List(request):
	targets = Target.objects.all()
	context = {
		'targets':targets
	}
	return render(request,'admin-panel/movement/target_list.html',context)


@user_passes_test(check_staff)
def Edit_Target(request,id):
	select_target = Target.objects.get(id=id)
	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		code = request.POST['code']
		price = request.POST['price']
		name = request.POST['name']
		target = Target.objects.filter(Q(name=name) | Q(code=code)).exclude(id =select_target.id)
		if target.count() != 0 :
			context = {
				'select_target':select_target,
				'error': True,
				'message': 'مقصد با اطلاعات وارد شده وجود دارد. لطفا از یکتایی کد و نام مقصد اطمینان حاصل فرمایید'
			}
			return render(request, 'admin-panel/movement/edit_target.html', context)
		else:
			select_target.price = price
			select_target.code = code
			select_target.name = name
			select_target.save()
			message = 'مقصد با نام "{}" و کد {} با موفقیت تغییر یافت.'.format(select_target.name, select_target.code)
			context = {
				'select_target':select_target,
				'success': True,
				'message': message
			}
			return render(request, 'admin-panel/movement/edit_target.html', context)
	context = {
		'select_target':select_target
	}
	return render(request,'admin-panel/movement/edit_target.html',context)


@user_passes_test(check_staff)
def Add_Driver(request):
	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')
		code = request.POST['code']
		name = request.POST['first_name']
		last_name = request.POST['last_name']
		national_number = request.POST['national_number']
		phone_number = request.POST['phone_number']
		try:
			driver = Driver.objects.get(code=code)
			message = 'راننده با کد {} در سیستم وجود دارد.'.format(national_number)
			info = 'برای ویرایش اطلاعات اینجا کلیک کنید!'
			context = {
				'info': info,
				'message': message,
				'select_driver': driver,
				'error': True,
			}
			return render(request, 'admin-panel/payment/add_driver.html', context)
		except:
			pass
		try:
			driver = Driver.objects.get(national_number=national_number)
			message = 'راننده با شماره ملی {} در سیستم وجود دارد.'.format(national_number)
			info = 'برای ویرایش اطلاعات اینجا کلیک کنید!'
			context = {
				'info':info,
				'message':message,
				'select_driver':driver,
				'error':True,
			}
			return render(request,'admin-panel/payment/add_driver.html',context)
		except:
			driver = Driver.objects.create(code=code,first_name=name,last_name=last_name,national_number=national_number,phone_number=phone_number)
			message = 'راننده {} با موفقیت به لیست اشخاص اضافه شد.'.format(driver.user_id.get_full_name())

			info = 'برای ویرایش اطلاعات اینجا کلیک کنید'
			context = {
				'info':info,
				'success':True,
				'message':message,
				'select_driver':driver
			}
			return render(request,'admin-panel/payment/add_driver.html',context)

	context = {

	}
	return render(request,'admin-panel/payment/add_driver.html',context)


@user_passes_test(check_staff)
def Edit_Driver(request,id):
	select_driver = Driver.objects.get(id=id)
	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		code = request.POST['code']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		national_number = request.POST['national_number']
		phone_number = request.POST['phone_number']
		select_driver.code = code
		select_driver.first_name = first_name
		select_driver.last_name = last_name
		select_driver.phone_number = phone_number
		select_driver.national_number = national_number
		select_driver.save()
		message = 'مشخصات {} با موفقیت تغییر یافت.'.format(select_driver.user_id.get_full_name())
		context ={
			'select_driver':select_driver,
			'success':True,
			'message':message

		}
		return render(request,'admin-panel/movement/edit_driver.html',context)
	context = {
		'select_driver':select_driver
	}
	return render(request,'admin-panel/movement/edit_driver.html',context)


@user_passes_test(check_staff)
def Driver_List(request):

	drivers = Driver.objects.all()
	movement_services = Movement_Service.objects.all()
	services_counter = {}

	for driver in drivers:
		services_counter[driver.id] = 0
		for service in movement_services:
			if driver == service.driver_id:
				services_counter[service.driver_id.id] += 1


	context = {
		'services':services_counter,
		'drivers':drivers,

	}
	return render(request,'admin-panel/payment/dirvers_list.html',context)


@user_passes_test(check_staff)
def Movement_List(request):
	services = Movement_Service.objects.all()
	context = {
		'services':services
	}
	return render(request,'admin-panel/movement/movement_list.html',context)