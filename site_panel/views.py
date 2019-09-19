from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from .models import *
from datetime import datetime

from jdatetime import JalaliToGregorian, GregorianToJalali



def Quick_Deceased(request):
	if request.user.is_authenticated and request.user.is_staff:
		cities = City.objects.all()
		if request.method == 'POST':

			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			fa_name = request.POST['fa_name']
			identification_number = request.POST['identification_number']
			national_number = request.POST['national_number']
			birth_day_r = request.POST['birth_day']
			try:
				birth_day_miladi = datetime.strptime(birth_day_r, '%Y-%m-%d')
				day = birth_day_miladi.day
				year = birth_day_miladi.year
				month = birth_day_miladi.month
				birth_day = JalaliToGregorian(year, month, day)
				birth_day = birth_day.getGregorianList()
				year = birth_day[0]
				month = birth_day[1]
				day = birth_day[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				birth_day = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				birth_day = None
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
			try:
				date_of_death_miladi = datetime.strptime(date_of_death, '%Y-%m-%d')
				day = date_of_death_miladi.day
				year = date_of_death_miladi.year
				month = date_of_death_miladi.month
				date_of_death = JalaliToGregorian(year, month, day)
				date_of_death = date_of_death.getGregorianList()
				year = date_of_death[0]
				month = date_of_death[1]
				day = date_of_death[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				date_of_death = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				date_of_death = None
			cause_death = request.POST['cause_death']


			try:
				picture = request.FILES['presenter_document']
			except:
				picture = None

			place = None
			try:
				location = request.POST['location']
			except:
				location = ''
			code = ''
			block = ''
			radif = ''
			number = ''
			floor = ''
			place_type = ''
			latitude = ''
			longitude = ''
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
				try:
					place = Place.objects.get(code=code)
					place_save = False
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
						place_save = True
				except:
					if code != '' and block != '' and radif != '' and number != '' and floor != '' and place_type != '':
						place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
													 type=place_type, longitude=longitude, latitude=latitude)
					else:
						context = {
							'cities': cities,
							'error': True,
							'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
						}
						return render(request, 'admin-panel/online-deceased.html', context)

			if len(national_number) != 11 or len(presenter_national_number) != 11:
				context = {
					'first_name':first_name,
					'birth_day':birth_day_r,
					'last_name':last_name,
					'fa_name':fa_name,
					'identification_number':identification_number,
					'national_number':national_number,
					'bio':bio,
					'code':code,
					'block':block,
					'radif':radif,
					'number':number,
					'location':location,



					'error': True,
					'message': 'کد ملی به صورت صحیح وارد نشده است!',
				}
				return render(request, 'admin-panel/quick-deceased.html', context)

			try:
				deceased = Deceased.objects.get(national_number=national_number)
				context = {
					'error': True,
					'message': 'متوفی با این شماره ملی قبلا ثبت شده است!',
					'info': 'اگر قصد تغییر مشخصات متوفی با این شماره ملی را دارید اینجا کلیک کنید',
					'link': deceased
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
											   identification_number=identification_number, bio=bio,
											   date_of_birth=birth_day)
			deceased.presenter_id = presenter
			deceased.save()

			place = None
			try:
				place = Place.objects.get(code=code)
				if place.status == 'Pre_sell' or place.status == 'Sold':
					context = {
						'error': True,
						'message': 'قبر انتخابی خالی نمیباشد.',
						'info': 'اگر قصد تغییر مشخصات متوفی دارید از لیست متوفی اقدام کنید',
					}
					return render(request, 'admin-panel/quick-deceased.html', context)
				else:
					place.status = 'Sold'
					place.save()
			except:
				place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
											 type=place_type, longitude=longitude, latitude=latitude)

			if place_save:
				place.save()
			license = License.objects.get(deceased_id=deceased)
			license.place_id = place
			license.picture = picture
			license.license_status = 'CONFIRMED'
			license.save()

			death_certificate = Death_Certificate.objects.get(deceased_id=deceased)
			death_certificate.doctor_first_name = doctor_first_name
			death_certificate.doctor_last_name = doctor_last_name
			death_certificate.medical_system_number = medical_system_number
			death_certificate.death_certificate_number = death_certificate_number
			death_certificate.date_of_death = date_of_death
			death_certificate.cause_death = cause_death
			death_certificate.status = 'Accepted'
			death_certificate.save()
			message = 'متوفی ' + deceased.get_full_name() + ' با موفقیت ثبت شد'
			context = {
				'success': True,
				'message': message,
				'info': 'برای ویرایش اطلاعات وارد شده اینجا کلیک کنید.',
				'deceased': deceased
			}
			return render(request, 'admin-panel/quick-deceased.html', context)
		warnings = ['لطفا همه موارد ستاره دار را با دقت پر کنید.',
					'پس از وارد کردن متوفی لطفا جهت وارد کردن هزینه قبر آن اقدام نمایید.',
					'اگر متوفی قبلا در سیستم ثبت شده است و قصد ویرایش اطلاعات دارید از طریق لیست متوفی اقدام کنید.']
		context = {
			'warnings': warnings,
			'cities':cities,

		}
		return render(request, 'admin-panel/quick-deceased.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/quick-new-deceased/')


def Online_Deceased(request):
	if request.user.is_authenticated and request.user.is_staff:
		cities = City.objects.all()

		if request.method == 'POST':
			license_status = None

			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			fa_name = request.POST['fa_name']
			identification_number = request.POST['identification_number']
			national_number = request.POST['national_number']
			birth_day = request.POST['birth_day']

			try:
				birth_day_miladi = datetime.strptime(birth_day, '%Y-%m-%d')
				day = birth_day_miladi.day
				year = birth_day_miladi.year
				month = birth_day_miladi.month
				birth_day = JalaliToGregorian(year, month, day)
				birth_day = birth_day.getGregorianList()
				year = birth_day[0]
				month = birth_day[1]
				day = birth_day[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				birth_day = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				birth_day = None
			try:
				address = request.POST['address']
			except:
				address = ''
			deceased_status = request.POST['deceased_status']
			deceased_type = request.POST['deceased_type']
			place_of_birth = request.POST['place_of_birth']
			issue_date = request.POST['issue_date']
			try:
				issue_date_miladi = datetime.strptime(issue_date, '%Y-%m-%d')
				day = issue_date_miladi.day
				year = issue_date_miladi.year
				month = issue_date_miladi.month
				issue_date = JalaliToGregorian(year, month, day)
				issue_date = issue_date.getGregorianList()
				year = issue_date[0]
				month = issue_date[1]
				day = issue_date[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				issue_date = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				issue_date = None
			mo_name = request.POST['mo_name']
			sex = request.POST['sex']
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
			try:
				date_of_death_miladi = datetime.strptime(date_of_death, '%Y-%m-%d')
				day = date_of_death_miladi.day
				year = date_of_death_miladi.year
				month = date_of_death_miladi.month
				date_of_death = JalaliToGregorian(year, month, day)
				date_of_death = date_of_death.getGregorianList()
				year = date_of_death[0]
				month = date_of_death[1]
				day = date_of_death[2]
				make_format = str(year) + '-' + str(month) + '-' + str(day)
				date_of_death = datetime.strptime(make_format, '%Y-%m-%d')
			except:
				date_of_death = None

			cause_death = request.POST['cause_death']
			death_certificate_stats = request.POST['death_certificate_stats']

			if first_name == '' or last_name == '' or presenter_first_name == '' or presenter_last_name == '' or doctor_first_name == '' or doctor_last_name == '':
				context = {
					'cities': cities,
					'error': True,
					'message': 'لطفا نام و نام خانوادگی متوفی یا معرف و پزشک را وارد کنید! لطفا همه موارد ستاره دار را به دقت پر کنید',
				}
				return render(request, 'admin-panel/online-deceased.html', context)

			if len(national_number) != 10 or len(presenter_national_number) != 10:
				context = {
					'cities': cities,
					'error': True,
					'message': 'کد ملی باید 11 رقمی باشد، لطفا نسبت به تصحیح آن اقدام فرمایید!'
				}
				return render(request, 'admin-panel/online-deceased.html', context)



			place = None
			try:
				location = request.POST['location']
			except:
				location = ''
			code = ''


			try:
				picture = request.FILES['presenter_document']
			except:
				picture = None

			try:
				deceased = Deceased.objects.get(national_number=national_number)
				context = {
					'cities': cities,
					'error': True,
					'message': 'متوفی با این شماره ملی قبلا ثبت شده است!',
					'info': 'اگر قصد تغییر مشخصات متوفی با این شماره ملی را دارید اینجا کلیک کنید',
					'link': deceased
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
				buyer = Buyer.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
											 national_number=presenter_national_number,
											 identification_number=presenter_identification_number,
											 phone_number=presenter_phone_number)

			deceased = Deceased.objects.create(national_number=national_number, first_name=first_name,
											   last_name=last_name, fa_name=fa_name,
											   identification_number=identification_number, bio=bio,
											   date_of_birth=birth_day, address=address,
											   deceased_status=deceased_status, deceased_type=deceased_type,
											   place_of_birth=place_of_birth,
											   issue_date=issue_date, mo_name=mo_name, sex=sex)
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
					if code != '' and block != '' and radif != '' and number != '' and floor != '' and place_type != '':
						place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
													 type=place_type, longitude=longitude, latitude=latitude)
					else:
						context = {
							'cities': cities,
							'error': True,
							'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
						}
						return render(request, 'admin-panel/online-deceased.html', context)

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
					place_service = Place_Service.objects.create(buyer_id=buyer, place_id=place, deceased_id=deceased,
																 payment_status='PAID')
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
			'cities': cities,
			'warnings': warnings,

		}
		return render(request, 'admin-panel/online-deceased.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/online-new-deceased/')


def Deceased_List(request):
	if request.user.is_authenticated and request.user.is_staff:

		deceaseds = Deceased.objects.all()

		context = {
			'deceaseds': deceaseds,
		}

		return render(request, 'admin-panel/deceased-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/quick-new-deceased/')


def Edit_Deceased(request, id):
	select_deceased = Deceased.objects.get(pk=id)
	license = License.objects.get(deceased_id=select_deceased)
	cities = City.objects.all()
	certificate = Death_Certificate.objects.get(deceased_id=select_deceased)
	# place_deceased = Place.objects.get()
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		fa_name = request.POST['fa_name']
		identification_number = request.POST['identification_number']
		national_number = request.POST['national_number']
		birth_day = request.POST['birth_day']

		try:
			birth_day_miladi = datetime.strptime(birth_day, '%Y-%m-%d')
			day = birth_day_miladi.day
			year = birth_day_miladi.year
			month = birth_day_miladi.month
			birth_day = JalaliToGregorian(year, month, day)
			birth_day = birth_day.getGregorianList()
			year = birth_day[0]
			month = birth_day[1]
			day = birth_day[2]
			make_format = str(year) + '-' + str(month) + '-' + str(day)
			birth_day = datetime.strptime(make_format, '%Y-%m-%d')
		except:
			birth_day = None
		try:
			address = request.POST['address']
		except:
			address = ''
		deceased_status = request.POST['deceased_status']
		deceased_type = request.POST['deceased_type']
		place_of_birth = request.POST['place_of_birth']
		issue_date = request.POST['issue_date']
		try:
			issue_date_miladi = datetime.strptime(issue_date, '%Y-%m-%d')
			day = issue_date_miladi.day
			year = issue_date_miladi.year
			month = issue_date_miladi.month
			issue_date = JalaliToGregorian(year, month, day)
			issue_date = issue_date.getGregorianList()
			year = issue_date[0]
			month = issue_date[1]
			day = issue_date[2]
			make_format = str(year) + '-' + str(month) + '-' + str(day)
			issue_date = datetime.strptime(make_format, '%Y-%m-%d')
		except:
			issue_date = None
		mo_name = request.POST['mo_name']
		sex = request.POST['sex']
		bio = request.POST['bio']





		presenter_first_name = request.POST['presenter_first_name']
		presenter_last_name = request.POST['presenter_last_name']
		presenter_phone_number = request.POST['presenter_phone_number']
		presenter_national_number = request.POST['presenter_national_number']
		presenter_identification_number = request.POST['presenter_identification_number']
		try:
			picture = request.FILES['presenter_document']
		except:
			picture = None

		license_status = request.POST['license_status']


		doctor_first_name = request.POST['doctor_first_name']
		doctor_last_name = request.POST['doctor_last_name']
		medical_system_number = request.POST['medical_system_number']
		death_certificate_number = request.POST['death_certificate_number']
		date_of_death = request.POST['date_of_death']
		cause_death = request.POST['cause_death']
		death_certificate_stats = request.POST['death_certificate_stats']

		if first_name == '' or last_name == '' or presenter_first_name == '' or presenter_last_name == '' or doctor_first_name == '' or doctor_last_name == '':
			context = {
				'cities': cities,
				'error': True,
				'message': 'لطفا نام و نام خانوادگی متوفی یا معرف و پزشک را وارد کنید! لطفا همه موارد ستاره دار را به دقت پر کنید',
			}
			return render(request, 'admin-panel/online-deceased.html', context)

		if len(national_number) != 10 or len(presenter_national_number) != 10:
			context = {
				'cities': cities,
				'error': True,
				'message': 'کد ملی باید 11 رقمی باشد، لطفا نسبت به تصحیح آن اقدام فرمایید!'
			}
			return render(request, 'admin-panel/online-deceased.html', context)



		place = None
		try:
			location = request.POST['location']
		except:
			location = ''
		code = ''

		place_save = False
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
					deceased = None
					try:
						deceased = place.license.select_related().get(deceased_id=select_deceased)
						deceased_full = True
					except:
						deceased_full = False
					if deceased_full :
						if deceased.deceased_id == select_deceased:
							pass
						else:
							context = {
								'cities': cities,
								'error': True,
								'message': 'قبر انتخابی خالی نمیباشد.',
								'info': 'برای دیدن لیست قبور شهرداری اینجا کلیک کنید!',
							}
							return render(request, 'admin-panel/quick-deceased.html', context)
					else:
						context = {
							'cities': cities,
							'error': True,
							'message': 'قبر انتخابی پیش فروش شده است.',
							'info': 'برای دیدن لیست قبور شهرداری اینجا کلیک کنید!',
						}
						return render(request, 'admin-panel/quick-deceased.html', context)
				else:
					place.status = 'Sold'
					place_save = True

			except:
				if code != '' and block != '' and radif != '' and number != '' and floor != '' and place_type != '':
					place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
												 type=place_type, longitude=longitude, latitude=latitude)

				else:
					context = {
						'cities': cities,
						'error': True,
						'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
					}
					return render(request, 'admin-panel/online-deceased.html', context)

		if place_save:
			place.save()


		select_deceased.first_name = first_name
		select_deceased.last_name = last_name
		select_deceased.fa_name = fa_name
		select_deceased.identification_number = identification_number
		select_deceased.national_number = national_number
		select_deceased.date_of_birth = birth_day
		select_deceased.deceased_status = deceased_status
		select_deceased.deceased_type = deceased_type
		select_deceased.place_of_birth = place_of_birth
		select_deceased.issue_date = issue_date
		select_deceased.mo_name = mo_name
		select_deceased.sex = sex
		select_deceased.bio = bio
		buyer = None
		try:
			presenter = Presenter.objects.get(national_number=presenter_national_number)
			presenter.first_name = presenter_first_name
			presenter.last_name = presenter_last_name
			presenter.national_number = presenter_national_number
			presenter.identification_number = presenter_identification_number
			presenter.phone_number = presenter_phone_number
			presenter.save()
		except:
			presenter = Presenter.objects.create(first_name=presenter_first_name,last_name=presenter_last_name,national_number=presenter_national_number,identification_number=presenter_identification_number
												 ,phone_number=presenter_phone_number)

		select_deceased.presenter_id = presenter
		try:
			buyer = Buyer.objects.get(national_number=presenter_national_number)
			buyer.first_name = presenter_first_name
			buyer.last_name = presenter_last_name
			buyer.national_number = presenter_national_number
			buyer.identification_number = presenter_identification_number
			buyer.phone_number = presenter_phone_number
			buyer.save()
		except:
			buyer = Buyer.objects.create(first_name=presenter_first_name,last_name=presenter_last_name,national_number=presenter_national_number,identification_number=presenter_identification_number
												 ,phone_number=presenter_phone_number)

		if location:
			license = License.objects.get(deceased_id=select_deceased)
			license.move_status = 'SEND-OUT'
			license.city_id = location
			license.picture = picture
			license.place_id = None
			license.license_status = license_status
			try:
				place_service = Place_Service.objects.get(deceased_id=select_deceased)
				if place_service.payment_status == 'PAID':
					place_service.deceased_id = None
					place_service.save()
				place_service.delete()
			except:
				pass
			license.save()
		else:
			license = License.objects.get(deceased_id=select_deceased)
			license.move_status = 'FERDOS-REZA'
			license.place_id = place
			license.picture = picture
			license.city_id = None
			license.license_status = license_status
			license.save()

			if license_status == 'CONFIRMED':
				try:
					place_service = Place_Service.objects.get(deceased_id=select_deceased)
					place_service.buyer_id = buyer
					place_service.payment_status = 'PAID'
					place_service.save()
				except:
					place_service = Place_Service.objects.create(buyer_id=buyer, place_id=place, deceased_id=select_deceased,
																 payment_status='PAID')
			else:
				pass

		select_deceased.save()

		certificate.doctor_first_name = doctor_first_name
		certificate.doctor_last_name = doctor_last_name
		certificate.death_certificate_number = death_certificate_number
		certificate.deceased_id = select_deceased
		certificate.status = death_certificate_stats
		certificate.date_of_death = date_of_death
		certificate.cause_death = cause_death
		certificate.medical_system_number = medical_system_number
		certificate.save()



	context = {
		'certificate':certificate,
		'cities':cities,
		'license': license,
		'select_deceased': select_deceased,
	}
	return render(request, 'admin-panel/edit-deceased-info.html', context)
