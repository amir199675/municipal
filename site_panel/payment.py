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


@user_passes_test(check_staff)
def User_list(request):

	if request.method == 'GET' and 'delete_data' in request.GET :
		users = MyUser.objects.all()
		for user in users:
			user.phone_number = None
			user.national_number = None
			user.save()
		return redirect('Site_Panel:user_list')

	if request.method == 'GET' and 'update_data' in request.GET :
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

	select_user = MyUser.objects.get(id = id)

	if request.method == 'POST':
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
	services = Service_List.objects.all()
	buyers = Buyer.objects.all()
	deceaseds = Deceased.objects.all()
	if request.method == 'POST':
		serves = request.POST.getlist('serves')
		# return HttpResponse(serves[0])
		str = ''
		for serve in serves:
			str += serve
		str = str.split('Amir:D')
		buyer = request.POST['buyer']
		buyer = Buyer.objects.get(id=buyer)
		deceased = request.POST['deceased']
		deceased = Deceased.objects.get(id=deceased)
		status = request.POST['status']
		document = RandForBill()
		# return HttpResponse(document)
		for i in str:
			if i != '':
				service = Service_List.objects.get(id=i)
				additional = Additional_Service.objects.create(service_id=service,buyer_id=buyer,status=status,deceased_id=deceased)

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