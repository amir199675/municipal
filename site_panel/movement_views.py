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
		targets = Target.objects.all()

		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')
			serves = request.POST.getlist('serves')
			# return HttpResponse(serves)
			# return HttpResponse(serves[0])
			strr = ''
			for serve in serves:
				strr += serve
			strr = strr.split('Amir:D')

			document = RandForBill()

			driver = request.POST['driver']
			try:
				driver_id = Driver.objects.get(id=driver)
			except:
				context = {

					'buyers': buyers,
					'cars': cars,
					'targets': targets,
					'select_deceased': select_deceased,
					'drivers': drivers,
					'error':True,
					'message':'لطفا راننده مورد نظر را انتخاب کنید'
				}
				return render(request, 'admin-panel/movement/movement_license.html', context)

			start_date = request.POST['date']
			car = request.POST['car']
			try:
				car_id = Car.objects.get(id = car)
			except:
				context = {

					'buyers': buyers,
					'cars': cars,
					'targets': targets,
					'select_deceased': select_deceased,
					'drivers': drivers,
					'error':True,
					'message':'لطفا ماشین حمل مورد نظر را انتخاب کنید'
				}
				return render(request, 'admin-panel/movement/movement_license.html', context)

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

			buyer_id = request.POST['buyer']
			buyer = None
			if buyer_id == '':

				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				phone_number = request.POST['phone_number']
				national_number = request.POST['national_number']
				if national_number == '':
					context = {

						'buyers': buyers,
						'cars': cars,
						'targets': targets,
						'select_deceased': select_deceased,
						'drivers': drivers,
						'error': True,
						'message': 'معرف مورد نظر را انتخاب کنید.'
					}
					return render(request,'admin-panel/movement/movement_license.html',context)
				try:
					buyer = Buyer.objects.create(first_name=first_name,last_name=last_name,phone_number=phone_number,national_number=national_number)
				except:
					return HttpResponse('خطا در ذخیره سازی اطلاعات معرف')
			else:
				buyer = Buyer.objects.get(id=buyer_id)
			for i in strr:
				if i != '':
					service = Target.objects.get(id=i)
					movement = Movement_Service.objects.create(target_id=service, buyer_id=buyer, status=status,
															   deceased_id=select_deceased,start_date=date,start_time=start_time
															   ,price=service.price,car_id=car_id,driver_id=driver_id)
			# return HttpResponse(strr)
			try:
				bills = Bill.objects.filter(deceased_id=select_deceased, movement_service_id__buyer_id = buyer,
											document__isnull=True)
				for bill in bills:
					bill.document = document
					bill.save()
			except:
				pass

			message = 'سرویس حمل و نقل با شماره فاکتور {} با موفقیت توسط {} ثبت شد.'.format(document,buyer.get_full_name())
			buyers = Buyer.objects.all()
			context = {
				'select_deceased':select_deceased,
				'buyers':buyers,
				'success':True,
				'message':message
			}
			return render(request, 'admin-panel/movement/movement_license.html', context)

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
def Census_Movement(request):

	targets = Target.objects.all()
	drivers = Driver.objects.all()

	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')
		start_date = request.POST['start_date']
		date_s = False
		date_e = False
		if start_date != '':
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
				start_date = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				start_date = None
		else:
			start_date = '1900-01-01'
			start_date = datetime.strptime(start_date, '%Y-%m-%d')

		end_date = request.POST['end_date']
		if end_date != '':
			try:
				end_date_miladi = datetime.strptime(end_date, '%Y/%m/%d')
				day = end_date_miladi.day
				year = end_date_miladi.year
				month = end_date_miladi.month
				date = JalaliToGregorian(year, month, day)
				date = date.getGregorianList()
				year = date[0]
				month = date[1]
				day = date[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				end_date = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				end_date = None
		else:
			end_date = datetime.now().date()

		# return HttpResponse(sex)
		try:
			target_id = request.POST['target']
		except:
			target_id = 'all'

		if target_id != 'all':
			target = Target.objects.get(id=target_id)
			target = target.name

		else:
			target = ''

		try:
			driver_id = request.POST['driver']
		except:
			driver_id = 'all'
		if driver_id != 'all' :
			driver_id = Driver.objects.get(id = driver_id)
			driver_id = driver_id.national_number
		else:
			# return HttpResponse(driver_id)
			driver_id = ''

		services = Movement_Service.objects.filter(target_id__name__contains=target,driver_id__national_number__contains=driver_id,start_date__gte=start_date,start_date__lte=end_date)
		total_price = 0
		for service in services:
			total_price += int(service.price)
		start_date = request.POST['start_date']
		if start_date != '':
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
				select_start = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				select_start = None
		else:
			select_start= ''

		end_date = request.POST['end_date']
		if end_date != '':
			try:
				end_date_miladi = datetime.strptime(end_date, '%Y/%m/%d')
				day = end_date_miladi.day
				year = end_date_miladi.year
				month = end_date_miladi.month
				date = JalaliToGregorian(year, month, day)
				date = date.getGregorianList()
				year = date[0]
				month = date[1]
				day = date[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				select_end = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				select_end = None
		else:
			select_end = ''

		error = False
		if services.count() == 0 :
			error = True
		select_target = target
		select_driver = driver_id
		# return HttpResponse(select_driver)
		context = {
			'total_price':total_price,
			'select_target':select_target,
			'select_driver':select_driver,
			'error':error,
			'drivers':drivers,
			'targets':targets,
			'select_start':select_start,
			'select_end':select_end,
			'services':services,
		}
		return render(request,'admin-panel//movement/movement_list.html',context)

	context = {
		'targets':targets,
		'drivers':drivers,

	}
	return render(request, 'admin-panel/movement/movement_list.html', context)
