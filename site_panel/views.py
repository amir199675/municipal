from django.shortcuts import render, HttpResponse ,redirect
from main.models import *
from .models import *
from datetime import datetime

from django.core.paginator import Paginator


def Quick_Deceased(request):
	if request.user.is_authenticated and request.user.is_staff :

		if request.method == 'POST':


			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			fa_name = request.POST['fa_name']
			identification_number = request.POST['identification_number']
			national_number = request.POST['national_number']
			birth_day = request.POST['birth_day']
			bio = request.POST['bio']

			code = request.POST['code']
			block = request.POST['block']
			radif = request.POST['radif']
			number = request.POST['number']
			floor = request.POST['floor']
			place_type = request.POST['place_type']
			latitude = request.POST['latitude']
			longitude = request.POST['longitude']

			presenter_first_name = request.POST['presenter_first_name']
			presenter_last_name = request.POST['presenter_last_name']
			presenter_phone_number = request.POST['presenter_phone_number']
			presenter_national_number = request.POST['presenter_national_number']
			presenter_identification_number = request.POST['presenter_identification_number']

			doctor_first_name = request.POST['doctor_first_name']
			doctor_last_name = request.POST['doctor_last_name']
			medical_system_number = request.POST['medical_system_number']
			death_certificate_number = request.POST['death_certificate_number']
			date_of_death = request.POST['date_of_death']
			cause_death = request.POST['cause_death']
			try:
				date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d')
			except:
				pass
			try:
				picture = request.FILES['presenter_document']
			except:
				picture = None

			if len(national_number) != 11 or len(presenter_national_number) != 11 :
				context = {
					'error':True,
					'message':'کد ملی به صورت صحیح وارد نشده است!'
				}
				return render(request, 'admin-panel/quick-deceased.html', context)

			try:
				deceased = Deceased.objects.get(national_number=national_number)
				context = {
					'error':True,
					'message':'متوفی با این شماره ملی قبلا ثبت شده است!',
					'info':'اگر قصد تغییر مشخصات متوفی با این شماره ملی را دارید اینجا کلیک کنید',
					'link':deceased
				}
				return render(request, 'admin-panel/quick-deceased.html', context)
			except:
				pass


			presenter = None
			try:
				presenter = Presenter.objects.get(national_number=presenter_national_number)
			except:
				presenter = Presenter.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
													 phone_number=presenter_phone_number,
													 national_number=presenter_national_number,
													 identification_number=presenter_identification_number)


			deceased = Deceased.objects.create(national_number=national_number, first_name=first_name,
											   last_name=last_name, fa_name=fa_name,
											   identification_number=identification_number, bio=bio,date_of_birth=birth_day	)
			deceased.presenter_id = presenter
			deceased.save()

			place = None
			try:
				place = Place.objects.get(code=code)
				if place.status == 'Pre_sell' or place.status == 'Sold':
					context = {
						'error':True,
						'message':'قبر انتخابی خالی نمیباشد.',
						'info':'اگر قصد تغییر مشخصات متوفی دارید از لیست متوفی اقدام کنید',
					}
					return render(request,'admin-panel/quick-deceased.html',context)
				else:
					place.status = 'Sold'
					place.save()
			except:
				place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
											 type=place_type,longitude=longitude,latitude=latitude)

			license = License.objects.get(deceased_id=deceased)
			license.place_id = place
			license.picture = picture
			license.license_status = 'CONFIRMED'
			license.save()

			death_certificate = Death_Certificate.objects.get(deceased_id=deceased)
			death_certificate.doctor_first_name = doctor_first_name
			death_certificate.doctor_last_name=doctor_last_name
			death_certificate.medical_system_number=medical_system_number
			death_certificate.death_certificate_number=death_certificate_number
			death_certificate.date_of_death=date_of_death
			death_certificate.cause_death=cause_death
			death_certificate.date_of_death =date_of_death
			death_certificate.status = 'Accepted'
			death_certificate.save()
			message = 'متوفی '+ deceased.get_full_name() +' با موفقیت ثبت شد'
			context = {
				'success':True,
				'message':message,
				'info':'برای ویرایش اطلاعات وارد شده اینجا کلیک کنید.',
				'deceased':deceased
			}
			return render(request,'admin-panel/quick-deceased.html',context)
		warnings = ['لطفا همه موارد ستاره دار را با دقت پر کنید.','پس از وارد کردن متوفی لطفا جهت وارد کردن هزینه قبر آن اقدام نمایید.','اگر متوفی قبلا در سیستم ثبت شده است و قصد ویرایش اطلاعات دارید از طریق لیست متوفی اقدام کنید.']
		context = {
			'warnings':warnings,

		}
		return render(request, 'admin-panel/quick-deceased.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/quick-new-deceased/')

def Online_Deceased (request):
	if request.user.is_authenticated and request.user.is_staff:
		cities = City.objects.all()

		if request.method == 'POST' :
			license_status = None

			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			fa_name = request.POST['fa_name']
			identification_number = request.POST['identification_number']
			national_number = request.POST['national_number']
			birth_day = request.POST['birth_day']
			bio = request.POST['bio']

			presenter_first_name = request.POST['presenter_first_name']
			presenter_last_name = request.POST['presenter_last_name']
			presenter_phone_number = request.POST['presenter_phone_number']
			presenter_national_number = request.POST['presenter_national_number']
			presenter_identification_number = request.POST['presenter_identification_number']

			doctor_first_name = request.POST['doctor_first_name']
			doctor_last_name = request.POST['doctor_last_name']
			medical_system_number = request.POST['medical_system_number']
			death_certificate_number = request.POST['death_certificate_number']
			date_of_death = request.POST['date_of_death']
			cause_death = request.POST['cause_death']
			death_certificate_stats = request.POST['death_certificate_stats']


			if first_name == '' or last_name == '' or presenter_first_name == '' or presenter_last_name == '' or doctor_first_name == '' or doctor_last_name == '' :
				context = {
					'cities':cities,
					'error':True,
					'message':'لطفا نام و نام خانوادگی متوفی یا معرف و پزشک را وارد کنید! لطفا همه موارد ستاره دار را به دقت پر کنید',
				}
				return render(request,'admin-panel/online-deceased.html',context)


			# if len(national_number) != 10 or len(presenter_national_number) != 10:
			# 	context = {
			# 		'cities': cities,
			# 		'error': True,
			# 		'message': 'کد ملی باید 11 رقمی باشد، لطفا نسبت به تصحیح آن اقدام فرمایید!'
			# 	}
			# 	return render(request, 'admin-panel/online-deceased.html', context)

			try:
				address = request.POST['address']
			except:
				address = ''
			deceased_status = request.POST['deceased_status']
			deceased_type = request.POST['deceased_type']
			place_of_birth = request.POST['place_of_birth']
			issue_date = request.POST['issue_date']
			mo_name = request.POST['mo_name']
			sex = request.POST['sex']

			place = None
			try:
				location = request.POST['location']
			except:
				location = ''
			code = ''

			try:
				issue_date = datetime.strptime(issue_date,'%Y-%m-%d')
			except:
				issue_date = None
			try:
				date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d')
			except:
				pass
			try:
				picture = request.FILES['presenter_document']
			except:
				picture = None


			try:
				deceased = Deceased.objects.get(national_number=national_number)
				context = {
					'cities': cities,
					'error':True,
					'message':'متوفی با این شماره ملی قبلا ثبت شده است!',
					'info':'اگر قصد تغییر مشخصات متوفی با این شماره ملی را دارید اینجا کلیک کنید',
					'link':deceased
				}
				return render(request, 'admin-panel/online-deceased.html', context)
			except:
				pass

			presenter = None
			try:
				presenter = Presenter.objects.get(national_number=presenter_national_number)
			except:
				presenter = Presenter.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
													 phone_number=presenter_phone_number,
													 national_number=presenter_national_number,
													 identification_number=presenter_identification_number)
				user = MyUser.objects.get(username=presenter_national_number)


			try:
				buyer = Buyer.objects.get(national_number=presenter_national_number)
			except:
				buyer = Buyer.objects.create(first_name=presenter_first_name,last_name=presenter_last_name,national_number=presenter_national_number,identification_number=presenter_identification_number,
											 phone_number=presenter_phone_number)


			deceased = Deceased.objects.create(national_number=national_number, first_name=first_name,
											   last_name=last_name, fa_name=fa_name,
											   identification_number=identification_number, bio=bio,
											   date_of_birth=birth_day,address=address,deceased_status=deceased_status,deceased_type=deceased_type,place_of_birth=place_of_birth,
											   issue_date=issue_date,mo_name=mo_name,sex=sex)
			deceased.presenter_id = presenter
			deceased.save()

			if location != '':
				location = request.POST['location']

			else:
				code = request.POST['code']
				block = request.POST['block']
				radif = request.POST['radif']
				number = request.POST['number']
				floor = request.POST['floor']
				place_type = request.POST['place_type']
				latitude = request.POST['latitude']
				longitude = request.POST['longitude']
				license_status = request.POST['license_status']
				try:
					place = Place.objects.get(code=code)
					if place.status == 'Pre_sell' or place.status == 'Sold':
						context = {
							'cities': cities,
							'error': True,
							'message': 'قبر انتخابی خالی نمیباشد.',
							'info': 'اگر قصد تغییر مشخصات متوفی دارید از لیست متوفی اقدام کنید',
						}
						return render(request, 'admin-panel/quick-deceased.html', context)
					else:
						place.status = 'Sold'
						place.save()
				except:
					if code != '' and block !='' and radif != '' and number != '' and floor != '' and place_type != '' :
						place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
													 type=place_type, longitude=longitude, latitude=latitude)
					else:
						context = {
							'cities': cities,
							'error': True,
							'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
						}
						return render(request,'admin-panel/online-deceased.html',context)





			if location:
				license = License.objects.get(deceased_id=deceased)
				license.move_status = 'SEND-OUT'
				license.city_id = location
				license.picture = picture
				license.license_status = license_status
				license.save()
			else:
				license = License.objects.get(deceased_id=deceased)
				license.move_status = 'FERDOS-REZA'
				license.place_id = place
				license.picture = picture
				license.license_status = license_status
				license.save()

				if license_status == 'CONFIRMED':
					place_service = Place_Service.objects.create(buyer_id=buyer,place_id=place,deceased_id=deceased,payment_status='PAID')
				else:
					pass


			death_certificate = Death_Certificate.objects.get(deceased_id=deceased)
			death_certificate.doctor_first_name = doctor_first_name
			death_certificate.doctor_last_name = doctor_last_name
			death_certificate.medical_system_number = medical_system_number
			death_certificate.death_certificate_number = death_certificate_number
			death_certificate.date_of_death = date_of_death
			death_certificate.cause_death = cause_death
			death_certificate.date_of_death = date_of_death
			death_certificate.status = death_certificate_stats
			death_certificate.save()
			message = 'متوفی ' + deceased.get_full_name() + ' با موفقیت ثبت شد'
			context = {
				'cities': cities,
				'success': True,
				'message': message,
				'info': 'برای ویرایش اطلاعات وارد شده اینجا کلیک کنید.',
				'deceased': deceased,

			}
			return render(request, 'admin-panel/online-deceased.html', context)
		warnings = ['لطفا همه موارد ستاره دار را با دقت پر کنید.',
					'پس از وارد کردن متوفی لطفا جهت وارد کردن هزینه قبر آن اقدام نمایید.',
					'اگر متوفی قبلا در سیستم ثبت شده است و قصد ویرایش اطلاعات دارید از طریق لیست متوفی اقدام کنید.']
		context = {
			'cities':cities,
			'warnings': warnings,

		}
		return render(request, 'admin-panel/online-deceased.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/online-new-deceased/')




def Deceased_List(request):
	if request.user.is_authenticated and request.user.is_staff:

		deceaseds = Deceased.objects.all()


		context = {
			'deceaseds':deceaseds,
		}

		return render(request,'admin-panel/all-deceaseds.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/quick-new-deceased/')

def Index(request):
	place_count = Place.objects.all().count()
	news = New.objects.all()[:5]
	ahadith = Hadith.objects.all()
	sliders = Slider.objects.filter(status='Active')
	black = False
	if sliders.count() == 0:
		black = True
	context = {
		'black':black,
		'sliders': sliders,
		'ahadith': ahadith,
		'news': news,
		'place_count': place_count,
	}
	return render(request, 'main-site/index.html', context)


def Memorial(request):
	marasems = Marasem.objects.all()
	context = {
		'marasems': marasems,
		'black': True
	}
	return render(request, 'main-site/memorial.html', context)
