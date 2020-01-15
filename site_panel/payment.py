from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from .models import *
from django.db.models import Q

from datetime import datetime
from django.contrib.auth.decorators import user_passes_test

from django.shortcuts import get_object_or_404

from jdatetime import JalaliToGregorian, GregorianToJalali

from seen.models import *
# from  site_panel.tasks import scheduler
# from  site_panel.tasks import amir


def check_staff(user):
	return user.is_staff


@user_passes_test(check_staff)
def User_list(request):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'لیست اشخاص'
		seen.counter = int(seen.counter) + 1
		seen.save()
	if request.method == 'GET' and 'delete_data' in request.GET :

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		users = MyUser.objects.all()
		for user in users:
			user.phone_number = None
			user.national_number = None
			user.save()
		return redirect('Site_Panel:user_list')

	if request.method == 'GET' and 'update_data' in request.GET :

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		users = MyUser.objects.all()
		for user in users:
			if user.presenter_id != '':
				try:
					de = Presenter.objects.get(id=user.presenter_id)
					user.phone_number = de.phone_number
					user.national_number = de.national_number
					user.save()
					print('presenter done!')
				except:
					pass

			if user.buyer_id != '':
				try:
					de = Buyer.objects.get(id=user.buyer_id)
					user.phone_number = de.phone_number
					user.national_number = de.national_number
					user.save()
					print('buyer done!')

				except:
					pass

			if user.deceased_id != '':
				try:
					de = Deceased.objects.get(id=user.deceased_id)
					user.national_number = de.national_number
					user.save()

					print('deceased done!')

				except:
					pass
		return redirect('Site_Panel:user_list')

	users = MyUser.objects.all()
	context = {
		'users':users
	}
	return render(request,'admin-panel/payment/user_list.html',context)


@user_passes_test(check_staff)
def Edit_User(request,id):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'ویرایش کاربر'
		seen.counter = int(seen.counter) + 1
		seen.save()
	select_user = MyUser.objects.get(id = id)

	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		phone_number = request.POST['phone_number']
		national_number = request.POST['national_number']
		select_user.first_name = first_name
		select_user.last_name = last_name
		select_user.phone_number = phone_number
		select_user.national_number = national_number
		select_user.save()
		if select_user.buyer_id != None:
			buyer = Buyer.objects.get(id = select_user.buyer_id)
			buyer.first_name = first_name
			buyer.last_name = last_name
			buyer.phone_number = phone_number
			buyer.national_number = national_number
			buyer.save()
		if select_user.presenter_id != None:
			presenter = Presenter.objects.get(id = select_user.presenter_id)
			presenter.first_name = first_name
			presenter.last_name = last_name
			presenter.phone_number = phone_number
			presenter.national_number = national_number
			presenter.save()
		if select_user.driver_id != None:
			driver = Driver.objects.get(id=select_user.driver_id)
			driver.first_name = first_name
			driver.last_name = last_name
			driver.phone_number = phone_number
			driver.national_number = national_number
			driver.save()
		select_user = MyUser.objects.get(id=id)
		context = {
			'select_user':select_user,
			'success':True,
			'message':'تغییرات با موفقیت انجام شد.'
		}
		return render(request,'admin-panel/payment/edit-user-info.html',context)

	context = {
		'select_user':select_user
	}
	return render(request,'admin-panel/payment/edit-user-info.html',context)


def RandForBill():
	while(True):
		number = random.randint(100000,999999)

		try:
			bill = Bill.objects.get(document=number)
		except:
			return number
@user_passes_test(check_staff)
def Reserve_Factor(request):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'ایجاد فاکتور'
		seen.counter = int(seen.counter) + 1
		seen.save()
	services = Service_List.objects.all()
	buyers = Buyer.objects.all()
	deceaseds = Deceased.objects.all()
	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		serves = request.POST.getlist('serves')
		# return HttpResponse(serves[0])
		str = ''
		for serve in serves:
			str += serve
		str = str.split('Amir:D')
		buyer = request.POST['buyer']
		try:
			buyer = Buyer.objects.get(id=buyer)
		except:
			context = {
				'error':True,
				'message':'لطفا خریدار را انتخاب کنید',
				'services':services,
				'deceaseds':deceaseds,
				'buyers':buyers
			}
			return render(request,'admin-panel/payment/factor-frosh.html',context)

		deceased = request.POST['deceased']
		try:
			deceased = Deceased.objects.get(id=deceased)
		except:
			context = {
				'error': True,
				'message': 'لطفا متوفی مورد نظر را انتخاب کنید',
				'services': services,
				'deceaseds': deceaseds,
				'buyers': buyers
			}
			return render(request, 'admin-panel/payment/factor-frosh.html', context)

		document = RandForBill()
		# return HttpResponse(document)
		for i in str:
			if i != '':
				service = Service_List.objects.get(id=i)
				additional = Additional_Service.objects.create(service_id=service,buyer_id=buyer,status='PAID',deceased_id=deceased)

		try:
			bills = Bill.objects.filter(deceased_id=deceased,additional_service_id__buyer_id=buyer,document__isnull=True)
			for bill in bills:
				bill.document = document
				bill.save()
		except:
			pass


		warnings = ['لطفا صفحه را رفرش نکنید، در غیر اینورت خدمات دوباره برای شما ثبت میشود!']

		message = 'فاکتور با شماره {} با موفقیت توسط {} ثبت شد'.format(document,buyer.get_full_name())
		services = Service_List.objects.all()
		context = {
			'services': services,
			'warnings': warnings,
			'success': True,
			'message': message,


		}
		return render(request, 'admin-panel/payment/factor-frosh.html', context)

	context = {
		'services':services,
		'deceaseds':deceaseds,
		'buyers':buyers
	}
	return render(request,'admin-panel/payment/factor-frosh.html',context)


@user_passes_test(check_staff)
def Factor_List(request):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'لیست فاکتورها'
		seen.counter = int(seen.counter) + 1
		seen.save()
	factors = Bill.objects.all().distinct('document')
	price = {}
	for factor in factors:
		bills = Bill.objects.filter(document=factor.document)
		price[factor.id] = 0
		for bill in bills:
			price[factor.id] = price[factor.id]+int(bill.price)
	context = {
		'price':price,
		'factors':factors
	}
	return render(request,'admin-panel/payment/factor-list.html',context)

@user_passes_test(check_staff)
def Factor_Details(request,document):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'نمایش فاکتور'
		seen.counter = int(seen.counter) + 1
		seen.save()
	bills = Bill.objects.filter(document=document)
	total_price = 0
	for bill in bills :
		total_price = total_price + int(bill.price)
	context = {
		'total_price':total_price,
		'bills':bills

	}
	return render(request,'admin-panel/payment/reserve-service-list.html',context)


def Add_Service(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
			seen.name = 'اضافه کردن خدمات اضافه'
			seen.counter = int(seen.counter) + 1
			seen.save()
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			code = request.POST['code']
			name = request.POST['name']
			price = request.POST['price']
			if name == '' and price == '' and code == '' :
				context = {
					'error': True,
					'message': 'لطفا همه فیلد ها را پر کنید.',

				}
				return render(request, 'admin-panel/add-service.html', context)
			try:
				service_list = Service_List.objects.get(code = code)
				context = {
					'error':True,
					'code':code,
					'name':name,
					'price':price,
					'message' : 'خدمات با این کد وجود دارد'
				}
				return render (request,'admin-panel/add-service.html',context)
			except:
				service_list = Service_List.objects.create(code = code,name=name,price=price)

			warnings = ['لطفا صفحه را رفرش نکنید، در غیر اینورت خدمات دوباره برای شما ثبت میشود!']
			message = 'خدمات "{}" با موفقیت اضافه شد'.format(service_list.name)
			context = {
				'warnings':warnings,
				'success':True,
				'message':message,

			}
			return render(request,'admin-panel/add-service.html',context)
		else:
			return render(request,'admin-panel/add-service.html')

	else:
		return redirect('/Account/login/?next=/Admin/add-service/')


def Services(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
			seen.name = 'لیست خدمات'
			seen.counter = int(seen.counter) + 1
			seen.save()
		services = Service_List.objects.all()
		context = {
			'services':services
		}
		return render(request,'admin-panel/service-list.html',context)
	else:
		return redirect(request,'/Account/login/?next=/Admin/service-list/')

def Edit_Service(request,id):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'اضافه کردن متوفی قدیمی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		select_service = Service_List.objects.get(id = id)
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			name = request.POST['name']
			code = request.POST['code']
			price = request.POST['price']
			if name == '' and code == '' and price == '':
				context = {
					'error': True,
					'message': 'لطفا همه فیلد ها را پر کنید.',

				}
				return render(request, 'admin-panel/edit-service.html', context)
			try:
				service = Service_List.objects.get(code=code)
				if select_service == service:
					service.code = code
					service.price = price
					service.name =name
					service.save()
					context = {
						'success': True,
						'message': 'تغییرات با موفقیت انجام شد!',
						'select_service': service
					}
					return render(request, 'admin-panel/edit-service.html', context)
				else:
					context = {
					'error':True,
					'message':'کدی ک وارد کردید در لیست خدمات وجود دارد!',
					'select_service':select_service

				}
					return render(request,'admin-panel/edit-service.html',context)
			except:
				select_service= Service_List.objects.get(pk=id)
				select_service.code = code
				select_service.price = price
				select_service.name = name
				select_service.save()
				context = {
					'success':True,
					'message':'تغییرات با موفقیت انجام شد!',
					'select_service':select_service
				}
				return render(request,'admin-panel/edit-service.html',context)
		context = {
			'select_service':select_service
		}
		return render(request,'admin-panel/edit-service.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/service-list/edit/{}/'.format(str(id)))

@user_passes_test(check_staff)
def Place_Pre_Sell(request):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'پیش فروش قبور'
		seen.counter = int(seen.counter) + 1
		seen.save()
	places = Place.objects.filter(status='Municipal')
	buyers = Buyer.objects.all()
	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		buyer = request.POST['buyer']
		request_places = request.POST.getlist('places')
		str = ''
		if buyer != '':
			buyer = Buyer.objects.get(id=buyer)
			for place in request_places:
				str += place
			str = str.split('Amir:D')
			for s in str:
				if s != '':
					place_service = Place_Service.objects.create(place_id_id=int(s),buyer_id=buyer,payment_status='PAID')

		else:
			name = request.POST['first_name']
			last_name = request.POST['last_name']
			phone_number = request.POST['phone_number']
			national_number = request.POST['national_number']
			try:
				buyer = Buyer.objects.get(national_number=national_number)
				context = {
					'error':True,
					'message':'شماره ملی وارد شده در بین خریداران وجود دارد، لطفا خریدار را از بین خریداران قبلی انتخاب کنید'
				}
				return render(request,'admin-panel/payment/place_pre_sell.html',context)
			except:
				buyer = Buyer.objects.create(first_name=name,last_name=last_name,national_number=national_number,phone_number=phone_number)
				for place in request_places:
					str += place
				str = str.split('Amir:D')
				for s in str:
					if s != '':
						place_service = Place_Service.objects.create(place_id_id=int(s), buyer_id=buyer,payment_status='PAID')
		places = Place.objects.filter(status='Municipal')
		buyers = Buyer.objects.all()
		message = 'پیش فروش قبر {} با موفقیت انجام شد.'.format(buyer.get_full_name())
		context = {
			'buyers':buyers,
			'places':places,
			'success':True,
			'message':message
		}
		return render(request,'admin-panel/payment/place_pre_sell.html',context)
	context = {
		'buyers':buyers,
		'places':places
	}
	return render(request,'admin-panel/payment/place_pre_sell.html',context)

@user_passes_test(check_staff)
def Add_User(request):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'اضافه کردن خریدار'
		seen.counter = int(seen.counter) + 1
		seen.save()
	if request.method == 'POST':

		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		name = request.POST['first_name']
		last_name = request.POST['last_name']
		national_number = request.POST['national_number']
		phone_number = request.POST['phone_number']
		try:
			buyer = Buyer.objects.get(national_number=national_number)
			message = 'خریدار با شماره ملی {} در سیستم وجود دارد.'.format(national_number)
			info = 'برای ویرایش اطلاعات اینجا کلیک کنید!'
			user = MyUser.objects.get(buyer_id=buyer.id)
			context = {
				'info':info,
				'message':message,
				'user':user,
				'error':True,
			}
			return render(request,'admin-panel/payment/add_user.html',context)
		except:
			buyer = Buyer.objects.create(first_name=name,last_name=last_name,national_number=national_number,phone_number=phone_number)
			message = 'خریدار {} با موفقیت به لیست اشخاص اضافه شد.'.format(buyer.get_full_name())
			user = MyUser.objects.get(buyer_id=buyer.id)
			info = 'برای ویرایش اطلاعات اینجا کلیک کنید'
			context = {
				'info':info,
				'success':True,
				'message':message,
				'user':user
			}
			return render(request,'admin-panel/payment/add_user.html',context)

	context = {

	}
	return render(request,'admin-panel/payment/add_user.html',context)

@user_passes_test(check_staff)
def Print_Factor(request,document):
	try:
		seen = Counter_Seen.objects.get(user_id=request.user, path=request.path)
		seen.counter = int(seen.counter) + 1
		seen.save()
	except:
		# return HttpResponse(request.user)
		seen = Counter_Seen.objects.create(user_id=request.user, path=request.path)
		seen.name = 'پرینت فاکتور'
		seen.counter = int(seen.counter) + 1
		seen.save()
	bills = Bill.objects.filter(document=document)
	total_price = 0
	for bill in bills:
		total_price = total_price + int(bill.price)
	context = {
		'total_price': total_price,
		'bills': bills

	}

	return render(request, 'admin-panel/payment/print_factor.html', context)
