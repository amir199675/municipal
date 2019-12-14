from django.shortcuts import render, HttpResponse, redirect
from main.models import *
from .models import *
from datetime import datetime

from django.shortcuts import get_object_or_404

from jdatetime import JalaliToGregorian, GregorianToJalali

import random

def RandForPlaceServiceDocument():
	while(True):
		number = random.randint(100000,999999)

		try:
			services = Place_Service.objects.get(document=number)
		except:
			return number

def Index(request):
	if request.user.is_authenticated and request.user.is_staff:

		context = {

		}
		return render(request,'admin-panel/index.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/')


def Quick_Deceased(request):
	if request.user.is_authenticated and request.user.is_staff:
		deceased = None

		if request.method == 'POST':

			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			fa_name = request.POST['fa_name']
			identification_number = request.POST['identification_number']
			national_number = request.POST['national_number']
			birth_day_r = request.POST['birth_day']

			try:
				birth_day_miladi = datetime.strptime(birth_day_r, '%Y/%m/%d')
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

			date_of_death_r = request.POST['date_of_death']
			try:
				date_of_death_miladi = datetime.strptime(date_of_death_r, '%Y/%m/%d')
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
			location_require = False
			if location != '':
				location = request.POST['location']
				location_require = True
			else:
				code = request.POST['code']
				block = request.POST['block']
				radif = request.POST['radif']
				number = request.POST['number']
				floor = request.POST['floor']
				place_type = request.POST['place_type']
				latitude = request.POST['latitude']
				longitude = request.POST['longitude']

			if first_name == '' or last_name == '' :
				context = {
					'first_name': first_name,
					'birth_day': birth_day_r,
					'last_name': last_name,
					'fa_name': fa_name,
					'identification_number': identification_number,
					'national_number': national_number,

					'bio': bio,
					'code': code,

					'bloock': block,
					'radif': radif,
					'number': number,
					'location': location,
					'floor': floor,
					'place_type': place_type,
					'latitude': latitude,
					'longitude': longitude,

					'error': True,
					'message': 'لطفا نام و نام خانوادگی متوفی یا معرف و پزشک را وارد کنید! لطفا همه موارد ستاره دار را به دقت پر کنید',
				}
				return render(request, 'admin-panel/quick-deceased.html', context)

			place_save = False
			place = None
			if location_require:
				pass
			else:
				try:
					place = Place.objects.get(code=code)

					if place.status == 'Pre_sell' or place.status == 'Sold':
						context = {
							'first_name': first_name,
							'birth_day': birth_day_r,
							'last_name': last_name,
							'fa_name': fa_name,
							'identification_number': identification_number,
							'national_number': national_number,

							'bio': bio,
							'code': code,
							'bloock': block,
							'radif': radif,
							'number': number,
							'location': location,
							'floor': floor,
							'place_type': place_type,
							'latitude': latitude,
							'longitude': longitude,

							'date_of_death': date_of_death_r,

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
							'first_name': first_name,
							'birth_day': birth_day_r,
							'last_name': last_name,
							'fa_name': fa_name,
							'identification_number': identification_number,
							'national_number': national_number,

							'bio': bio,
							'code': code,

							'bloock': block,
							'radif': radif,
							'number': number,
							'location': location,
							'floor': floor,
							'place_type': place_type,
							'latitude': latitude,
							'longitude': longitude,

							'date_of_death': date_of_death_r,

							'error': True,
							'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
						}
						return render(request, 'admin-panel/quick-deceased.html', context)
			if national_number != '' :
				try:

					deceased = Deceased.objects.get(national_number=national_number)
					context = {

						'first_name': first_name,
						'birth_day': birth_day_r,
						'last_name': last_name,
						'fa_name': fa_name,
						'identification_number': identification_number,
						'national_number': national_number,

						'bio': bio,
						'code': code,
						'bloock': block,
						'radif': radif,
						'number': number,
						'location': location,
						'floor': floor,
						'place_type': place_type,
						'latitude': latitude,
						'longitude': longitude,

						'date_of_death': date_of_death_r,

						'error': True,
						'message': 'متوفی با این شماره ملی قبلا ثبت شده است!',
						'info': 'اگر قصد تغییر مشخصات متوفی با این شماره ملی را دارید اینجا کلیک کنید',
						'link': deceased
					}
					return render(request, 'admin-panel/quick-deceased.html', context)
				except:
					pass
			if national_number != '':
				if len(national_number) != 10:
					context = {
						'first_name': first_name,
						'birth_day': birth_day_r,
						'last_name': last_name,
						'fa_name': fa_name,
						'identification_number': identification_number,
						'national_number': national_number,

						'bio': bio,
						'code': code,

						'bloock': block,
						'radif': radif,
						'number': number,
						'location': location,
						'floor': floor,
						'place_type': place_type,
						'latitude': latitude,
						'longitude': longitude,

						'error': True,
						'message': 'کد ملی باید 10 رقمی باشد.',
					}
					return render(request, 'admin-panel/quick-deceased.html', context)

				deceased = Deceased.objects.create(national_number=national_number,first_name=first_name,
												   last_name=last_name, fa_name=fa_name,
												   identification_number=identification_number, bio=bio,
												   date_of_birth=birth_day)
			else:
				deceased = Deceased.objects.create(first_name=first_name,
												   last_name=last_name, fa_name=fa_name,
												   identification_number=identification_number, bio=bio,
												   date_of_birth=birth_day)


			if place_save:
				place.save()
			place_service = None
			if location:
				license = License.objects.get(deceased_id=deceased)
				license.move_status = 'SEND-OUT'
				license.city_name = location
				license.picture = picture
				license.license_status = 'CONFIRMED'
				license.save()
			else:
				place_service = Place_Service.objects.create(place_id=place,deceased_id=deceased,document=RandForPlaceServiceDocument(),payment_status='PAID')

				license = License.objects.get(deceased_id=deceased)
				license.move_status = 'FERDOS-REZA'
				license.place_id = place
				license.picture = picture
				license.license_status = 'CONFIRMED'
				license.save()


			death_certificate = Death_Certificate.objects.get(deceased_id=deceased)

			death_certificate.date_of_death = date_of_death

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

		}
		return render(request, 'admin-panel/quick-deceased.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/quick-new-deceased/')


def Online_Deceased(request):
	if request.user.is_authenticated and request.user.is_staff:

		if request.method == 'POST':
			license_status = request.POST['license_status']

			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			fa_name = request.POST['fa_name']
			identification_number = request.POST['identification_number']
			national_number = request.POST['national_number']
			birth_day_r = request.POST['birth_day']

			try:
				birth_day_miladi = datetime.strptime(birth_day_r, '%Y/%m/%d')
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

			muni_code = request.POST['muni_code']
			place_of_birth = request.POST['place_of_birth']
			issue_date_r = request.POST['issue_date']
			try:
				issue_date_miladi = datetime.strptime(issue_date_r, '%Y/%m/%d')
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
			presenter_address = request.POST['presenter_address']

			doctor_first_name = request.POST['doctor_first_name']
			doctor_last_name = request.POST['doctor_last_name']
			medical_system_number = request.POST['medical_system_number']
			death_certificate_number = request.POST['death_certificate_number']
			date_of_death_r = request.POST['date_of_death']
			try:
				date_of_death_miladi = datetime.strptime(date_of_death_r, '%Y/%m/%d')
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
			location_require = False
			if location != '':
				location = request.POST['location']
				location_require = True
			else:
				code = request.POST['code']
				block = request.POST['block']
				radif = request.POST['radif']
				number = request.POST['number']
				floor = request.POST['floor']
				place_type = request.POST['place_type']
				latitude = request.POST['latitude']
				longitude = request.POST['longitude']
			if muni_code == '':
				context = {
					'first_name': first_name,
					'birth_day': birth_day_r,
					'last_name': last_name,
					'fa_name': fa_name,
					'mo_name': mo_name,
					'address': address,
					'identification_number': identification_number,
					'deceased_status': deceased_status,
					'muni_code': muni_code,
					'place_of_birth': place_of_birth,
					'issue_date': issue_date_r,
					'sex': sex,
					'license_status': license_status,
					'death_certificate_stats': death_certificate_stats,
					'national_number': national_number,
					'presenter_first_name': presenter_first_name,
					'presenter_last_name': presenter_last_name,
					'presenter_phone_number': presenter_phone_number,
					'presenter_national_number': presenter_national_number,
					'presenter_identification_number': presenter_identification_number,
					'presenter_address': presenter_address,
					'bio': bio,
					'code': code,
					'bloock': block,
					'radif': radif,
					'number': number,
					'location': location,
					'floor': floor,
					'place_type': place_type,
					'latitude': latitude,
					'longitude': longitude,
					'doctor_last_name': doctor_last_name,
					'doctor_first_name': doctor_first_name,
					'medical_system_number': medical_system_number,
					'death_certificate_number': death_certificate_number,
					'date_of_death': date_of_death_r,
					'cause_death': cause_death,

					'error': True,
					'message': 'لطفا شماره ثبت آرامستان را وارد کنید',
					'info': ''
				}
				return render(request, 'admin-panel/online-deceased.html', context)
			if first_name == '' or last_name == '' or presenter_first_name == '' or presenter_last_name == '' or doctor_first_name == '' or doctor_last_name == '':
				context = {
					'first_name': first_name,
					'birth_day': birth_day_r,
					'last_name': last_name,
					'fa_name': fa_name,
					'mo_name': mo_name,
					'address': address,
					'identification_number': identification_number,
					'deceased_status': deceased_status,
					'muni_code': muni_code,
					'place_of_birth': place_of_birth,
					'issue_date': issue_date_r,
					'sex': sex,
					'license_status': license_status,
					'death_certificate_stats': death_certificate_stats,
					'national_number': national_number,
					'presenter_first_name': presenter_first_name,
					'presenter_last_name': presenter_last_name,
					'presenter_phone_number': presenter_phone_number,
					'presenter_national_number': presenter_national_number,
					'presenter_identification_number': presenter_identification_number,
					'presenter_address': presenter_address,
					'bio': bio,
					'code': code,
					'bloock': block,
					'radif': radif,
					'number': number,
					'location': location,
					'floor': floor,
					'place_type': place_type,
					'latitude': latitude,
					'longitude': longitude,
					'doctor_last_name': doctor_last_name,
					'doctor_first_name': doctor_first_name,
					'medical_system_number': medical_system_number,
					'death_certificate_number': death_certificate_number,
					'date_of_death': date_of_death_r,
					'cause_death': cause_death,

					'error': True,
					'message': 'لطفا نام و نام خانوادگی متوفی یا معرف و پزشک را وارد کنید! لطفا همه موارد ستاره دار را به دقت پر کنید',
					'info': ''
				}
				return render(request, 'admin-panel/online-deceased.html', context)

			if len(national_number) != 10 or len(presenter_national_number) != 10:
				context = {
					'first_name': first_name,
					'birth_day': birth_day_r,
					'last_name': last_name,
					'fa_name': fa_name,
					'mo_name': mo_name,
					'address': address,
					'identification_number': identification_number,
					'deceased_status': deceased_status,
					'muni_code': muni_code,
					'place_of_birth': place_of_birth,
					'issue_date': issue_date_r,
					'sex': sex,
					'license_status': license_status,
					'death_certificate_stats': death_certificate_stats,
					'national_number': national_number,
					'presenter_first_name': presenter_first_name,
					'presenter_last_name': presenter_last_name,
					'presenter_phone_number': presenter_phone_number,
					'presenter_national_number': presenter_national_number,
					'presenter_identification_number': presenter_identification_number,
					'presenter_address': presenter_address,
					'bio': bio,
					'code': code,
					'bloock': block,
					'radif': radif,
					'number': number,
					'location': location,
					'floor': floor,
					'place_type': place_type,
					'latitude': latitude,
					'longitude': longitude,
					'doctor_last_name': doctor_last_name,
					'doctor_first_name': doctor_first_name,
					'medical_system_number': medical_system_number,
					'death_certificate_number': death_certificate_number,
					'date_of_death': date_of_death_r,
					'cause_death': cause_death,

					'error': True,
					'message': 'کد ملی باید 10 رقمی باشد، لطفا نسبت به تصحیح آن اقدام فرمایید!'
				}
				return render(request, 'admin-panel/online-deceased.html', context)

			try:
				picture = request.FILES['presenter_document']
			except:
				picture = None

			try:
				deceased = Deceased.objects.get(national_number=national_number)
				context = {
					'first_name': first_name,
					'birth_day': birth_day_r,
					'last_name': last_name,
					'fa_name': fa_name,
					'mo_name': mo_name,
					'address': address,
					'identification_number': identification_number,
					'deceased_status': deceased_status,
					'muni_code': muni_code,
					'place_of_birth': place_of_birth,
					'issue_date': issue_date_r,
					'sex': sex,
					'license_status': license_status,
					'death_certificate_stats': death_certificate_stats,
					'national_number': national_number,
					'presenter_first_name': presenter_first_name,
					'presenter_last_name': presenter_last_name,
					'presenter_phone_number': presenter_phone_number,
					'presenter_national_number': presenter_national_number,
					'presenter_identification_number': presenter_identification_number,
					'presenter_address': presenter_address,
					'bio': bio,
					'code': code,
					'bloock': block,
					'radif': radif,
					'number': number,
					'location': location,
					'floor': floor,
					'place_type': place_type,
					'latitude': latitude,
					'longitude': longitude,
					'doctor_last_name': doctor_last_name,
					'doctor_first_name': doctor_first_name,
					'medical_system_number': medical_system_number,
					'death_certificate_number': death_certificate_number,
					'date_of_death': date_of_death_r,
					'cause_death': cause_death,

					'error': True,
					'message': 'متوفی با این شماره ملی قبلا ثبت شده است!',
					'info': 'اگر قصد تغییر مشخصات متوفی با این شماره ملی را دارید اینجا کلیک کنید',
					'link': deceased
				}
				return render(request, 'admin-panel/online-deceased.html', context)
			except:
				pass

			place_save = False
			if location_require:
				pass
			else:
				try:
					place = Place.objects.get(code=code)

					if place.status == 'Pre_sell' or place.status == 'Sold':
						context = {
							'first_name': first_name,
							'birth_day': birth_day_r,
							'last_name': last_name,
							'fa_name': fa_name,
							'identification_number': identification_number,
							'national_number': national_number,
							'presenter_first_name': presenter_first_name,
							'presenter_last_name': presenter_last_name,
							'presenter_phone_number': presenter_phone_number,
							'presenter_national_number': presenter_national_number,
							'presenter_identification_number': presenter_identification_number,
							'presenter_address': presenter_address,
							'bio': bio,
							'code': code,
							'bloock': block,
							'radif': radif,
							'number': number,
							'location': location,
							'floor': floor,
							'place_type': place_type,
							'latitude': latitude,
							'longitude': longitude,
							'doctor_last_name': doctor_last_name,
							'doctor_first_name': doctor_first_name,
							'medical_system_number': medical_system_number,
							'death_certificate_number': death_certificate_number,
							'date_of_death': date_of_death_r,
							'cause_death': cause_death,

							'error': True,
							'message': 'قبر انتخابی خالی نمیباشد.',
							'info': 'اگر قصد تغییر مشخصات متوفی دارید از لیست متوفی اقدام کنید',
						}
						return render(request, 'admin-panel/online-deceased.html', context)
					else:
						place.status = 'Sold'
						place_save = True
				except:
					if code != '' and block != '' and radif != '' and number != '' and floor != '' and place_type != '':
						place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
													 type=place_type, longitude=longitude, latitude=latitude)
					else:
						context = {
							'first_name': first_name,
							'birth_day': birth_day_r,
							'last_name': last_name,
							'fa_name': fa_name,
							'identification_number': identification_number,
							'national_number': national_number,
							'presenter_first_name': presenter_first_name,
							'presenter_last_name': presenter_last_name,
							'presenter_phone_number': presenter_phone_number,
							'presenter_national_number': presenter_national_number,
							'presenter_identification_number': presenter_identification_number,
							'presenter_address':presenter_address,
							'bio': bio,
							'code': code,


							'bloock': block,
							'radif': radif,
							'number': number,
							'location': location,
							'floor': floor,
							'place_type': place_type,
							'latitude': latitude,
							'longitude': longitude,
							'doctor_last_name': doctor_last_name,
							'doctor_first_name': doctor_first_name,
							'medical_system_number': medical_system_number,
							'death_certificate_number': death_certificate_number,
							'date_of_death': date_of_death_r,
							'cause_death': cause_death,

							'error': True,
							'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
						}
						return render(request, 'admin-panel/online-deceased.html', context)

			presenter = None
			try:
				presenter = Presenter.objects.get(national_number=presenter_national_number)
			except:
				presenter = Presenter.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
													 phone_number=presenter_phone_number,
													 national_number=presenter_national_number,
													 identification_number=presenter_identification_number,address=presenter_address)
				user = MyUser.objects.get(username=presenter_national_number)




			deceased = Deceased.objects.create(national_number=national_number, first_name=first_name,
											   last_name=last_name, fa_name=fa_name,
											   identification_number=identification_number, bio=bio,
											   date_of_birth=birth_day, address=address,
											   deceased_status=deceased_status, muni_code=muni_code,
											   place_of_birth=place_of_birth,
											   issue_date=issue_date, mo_name=mo_name, sex=sex)
			deceased.presenter_id = presenter
			deceased.save()

			if place_save:
				place.save()

			if location:
				license = License.objects.get(deceased_id=deceased)
				license.move_status = 'SEND-OUT'
				license.city_name = location
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
				try:
					buyer = Buyer.objects.get(national_number=presenter_national_number)
				except:
					buyer = Buyer.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
												 national_number=presenter_national_number,
												 identification_number=presenter_identification_number,
												 phone_number=presenter_phone_number)
				if license_status == 'CONFIRMED':
					place_service = Place_Service.objects.create(buyer_id=buyer, place_id=place, deceased_id=deceased,document=RandForPlaceServiceDocument(),
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
				'success': True,
				'message': message,
				'info': 'برای ویرایش اطلاعات وارد شده اینجا کلیک کنید.',
				'deceased': deceased,

			}
			return render(request, 'admin-panel/online-deceased.html', context)
		warnings = ['لطفا همه موارد ستاره دار را با دقت پر کنید.',
					'پس از وارد کردن متوفی لطفا جهت وارد کردن هزینه قبر آن اقدام نمایید.',
					'اگر متوفی قبلا در سیستم ثبت شده است و قصد ویرایش اطلاعات دارید از طریق لیست متوفی اقدام کنید.']
		causes = Cause_Death.objects.all()
		context = {
			'causes':causes,
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
		return redirect('/Account/login/?next=/Admin/deceased-list/')



def Edit_Deceased(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		causes = Cause_Death.objects.all()
		buyer = None
		select_deceased = Deceased.objects.get(pk=id)
		license = License.objects.get(deceased_id=select_deceased)
		place_late = license.place_id
		service_late = None
		try:
			service_late = Place_Service.objects.get(place_id=place_late)
		except:
			pass
		certificate = Death_Certificate.objects.get(deceased_id=select_deceased)
		# place_deceased = Place.objects.get()
		if request.method == 'POST':
			place_change = False

			first_name = request.POST['first_name']
			last_name = request.POST['last_name']
			fa_name = request.POST['fa_name']
			identification_number = request.POST['identification_number']
			national_number = request.POST['national_number']
			birth_day_r = request.POST['birth_day']

			try:
				birth_day_miladi = datetime.strptime(birth_day_r, '%Y/%m/%d')
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
				# return HttpResponse(birth_day)
			except:
				birth_day = None
			try:
				address = request.POST['address']
			except:
				address = ''
			deceased_status = request.POST['deceased_status']
			muni_code = request.POST['muni_code']

			place_of_birth = request.POST['place_of_birth']
			issue_date_r = request.POST['issue_date']
			try:
				issue_date_miladi = datetime.strptime(issue_date_r, '%Y/%m/%d')
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
			presenter_address = request.POST['presenter_address']
			try:
				picture = request.FILES['presenter_document']
				pic = True
			except:
				picture = None
				pic = False

			license_status = request.POST['license_status']

			doctor_first_name = request.POST['doctor_first_name']
			doctor_last_name = request.POST['doctor_last_name']
			medical_system_number = request.POST['medical_system_number']
			death_certificate_number = request.POST['death_certificate_number']
			date_of_death_r = request.POST['date_of_death']
			try:
				date_of_death_miladi = datetime.strptime(date_of_death_r, '%Y/%m/%d')
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
				cause_death = Cause_Death.objects.get(name=cause_death)
			except:
				cause_death = None
			death_certificate_stats = request.POST['death_certificate_stats']

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
			location_require = False
			if location != '':
				location = request.POST['location']
				location_require = True
			else:
				code = request.POST['code']
				block = request.POST['block']
				radif = request.POST['radif']
				number = request.POST['number']
				floor = request.POST['floor']
				place_type = request.POST['place_type']
				latitude = request.POST['latitude']
				longitude = request.POST['longitude']

			place_save = False
			if location_require:
				pass
			else:
				try:
					place = Place.objects.get(code=code, block=block, radif=radif, number=number, floor=floor,
											  type=place_type, latitude=latitude, longitude=longitude)

					if place.status == 'Pre_sell' or place.status == 'Sold':
						deceased = None
						try:
							deceased = place.license.select_related().get(deceased_id=select_deceased)
							deceased_full = True
						except:
							deceased_full = False
						if deceased_full:
							if deceased.deceased_id == select_deceased:
								pass
							else:
								context = {
									'causes':causes,
									'error': True,
									'message': 'قبر انتخابی خالی نمیباشد.',
									'info': 'برای دیدن لیست قبور شهرداری اینجا کلیک کنید!',
								}
								return render(request, 'admin-panel/edit-deceased-info.html', context)
						else:
							context = {
								'causes': causes,
								'error': True,
								'message': 'قبر انتخابی پیش فروش شده است.',
								'info': 'برای دیدن لیست قبور شهرداری اینجا کلیک کنید!',
							}
							return render(request, 'admin-panel/edit-deceased-info.html', context)
					else:

						place.status = 'Sold'
						place_save = True

				except:
					if code != '' and block != '' and radif != '' and number != '' and floor != '' and place_type != '':
						try:
							place = Place.objects.create(code=code, block=block, radif=radif, number=number,
														 floor=floor,
														 type=place_type, longitude=longitude, latitude=latitude)
							try:
								service_late.delete()
							except:
								pass


						except:

							context = {
								'causes': causes,
								'select_deceased': select_deceased,
								'certificate': certificate,
								'license': license,
								'error': True,
								'message': 'لطفا نسبت به مشخصات وارد شده مربوط به قبر اطمینان حاصل فرمایید',
								'info': ''
							}
							return render(request, 'admin-panel/edit-deceased-info.html', context)
					else:
						context = {
							'causes': causes,
							'select_deceased': select_deceased,
							'certificate': certificate,
							'license': license,

							'error': True,
							'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
						}
						return render(request, 'admin-panel/edit-deceased-info.html', context)


			if first_name == '' or last_name == '' :
				context = {
					'causes': causes,
					'select_deceased': select_deceased,
					'certificate': certificate,
					'license': license,
					'error': True,
					'message': 'لطفا نام و نام خانوادگی متوفی را وارد کنید! ',
				}
				return render(request, 'admin-panel/edit-deceased-info.html', context)
			if national_number != '':

				try:

					deceased = Deceased.objects.get(national_number=national_number)

					if deceased.pk == select_deceased.pk:
						pass
					else:
						context = {

							'first_name': first_name,
							'birth_day': birth_day_r,
							'last_name': last_name,
							'fa_name': fa_name,
							'identification_number': identification_number,
							'national_number': national_number,

							'bio': bio,
							'code': code,
							'bloock': block,
							'radif': radif,
							'number': number,
							'location': location,
							'floor': floor,
							'place_type': place_type,
							'latitude': latitude,
							'longitude': longitude,

							'date_of_death': date_of_death_r,

							'error': True,
							'message': 'متوفی با این شماره ملی قبلا ثبت شده است!',
							'info': 'اگر قصد تغییر مشخصات متوفی با این شماره ملی را دارید اینجا کلیک کنید',
							'link': deceased
						}
						return render(request, 'admin-panel/edit-deceased-info.html', context)
				except:

					if len(national_number) != 10 :
						context = {
							'causes': causes,
							'select_deceased': select_deceased,
							'certificate': certificate,
							'license': license,
							'error': True,
							'message': 'کد ملی باید 10 رقمی باشد، لطفا نسبت به تصحیح آن اقدام فرمایید!'
						}
						return render(request, 'admin-panel/edit-deceased-info.html', context)

			if place_save:
				if place_late == place:
					place.save()
				else:
					service_late.delete()
					place.save()



			select_deceased.first_name = first_name
			select_deceased.last_name = last_name
			select_deceased.fa_name = fa_name
			select_deceased.identification_number = identification_number
			select_deceased.national_number = national_number
			select_deceased.date_of_birth = birth_day
			select_deceased.deceased_status = deceased_status
			select_deceased.address = address
			if muni_code != '':
				select_deceased.muni_code = muni_code
			else:
				select_deceased.muni_code = None
			select_deceased.place_of_birth = place_of_birth
			select_deceased.issue_date = issue_date
			select_deceased.mo_name = mo_name
			select_deceased.sex = sex
			select_deceased.bio = bio
			if presenter_national_number != '':
				if len(presenter_national_number) == 10:
					if presenter_last_name != '' or presenter_first_name != '':
						buyer = None
						try:
							presenter = Presenter.objects.get(national_number=presenter_national_number)
							presenter.first_name = presenter_first_name
							presenter.last_name = presenter_last_name
							presenter.national_number = presenter_national_number
							presenter.identification_number = presenter_identification_number
							presenter.phone_number = presenter_phone_number
							presenter.address = presenter_address
							presenter.save()
						except:
							presenter = Presenter.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
																 national_number=presenter_national_number,
																 identification_number=presenter_identification_number
																 , phone_number=presenter_phone_number,address=presenter_address)

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
							buyer = Buyer.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
														 national_number=presenter_national_number,
														 identification_number=presenter_identification_number
														 , phone_number=presenter_phone_number)
					else:
						context={
							'causes': causes,
							'select_deceased': select_deceased,
							'certificate': certificate,
							'license': license,
							'error':True,
							'message':'لطفا همه اطلاعات مربوط به متوفی را وارد کنید!'
						}
						return render(request,'admin-panel/edit-deceased-info.html',context)
				else:
					context = {
						'causes': causes,
						'select_deceased': select_deceased,
						'certificate': certificate,
						'license': license,
						'error': True,
						'message': 'لطفا کد ملی معرف را درست وارد کنید!!'
					}
					return render(request, 'admin-panel/edit-deceased-info.html', context)

			if location:
				license = License.objects.get(deceased_id=select_deceased)
				license.move_status = 'SEND-OUT'
				license.city_name = location
				if pic :
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
				if pic:
					license.picture = picture
				license.city_name = None
				license.license_status = license_status
				license.save()

				if license_status == 'CONFIRMED':
					try:
						place_service = Place_Service.objects.get(place_id=place)
						if place_service.deceased_id == None:
							place_service.buyer_id = buyer
							place_service.payment_status = 'PAID'
							place_service.save()
					except:
						place_service = Place_Service.objects.create(buyer_id=buyer, place_id=place,
																	 deceased_id=select_deceased,
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
			certificate.cause_death_id = cause_death
			certificate.medical_system_number = medical_system_number
			certificate.save()
			context = {
				'success': True,
				'message': 'تغییرات با موفقیت اعمال شد.',
				'causes': causes,
				'certificate': certificate,
				'license': license,
				'select_deceased': select_deceased,
			}
			return render(request, 'admin-panel/edit-deceased-info.html', context)

		context = {

			'causes': causes,
			'certificate': certificate,
			'license': license,
			'select_deceased': select_deceased,
		}
		return render(request, 'admin-panel/edit-deceased-info.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/edit-deceased-info/'+id)


def Add_Place(request):
	if request.user.is_authenticated and request.user.is_staff:
		if request.method == 'POST':
			code = request.POST['code']
			block = request.POST['block']
			radif = request.POST['radif']
			price = request.POST['price']
			number = request.POST['number']
			floor = request.POST['floor']
			place_type = request.POST['place_type']
			latitude = request.POST['latitude']
			longitude = request.POST['longitude']

			if code != '' and block != '' and radif != '' and number != '' and floor != '' and place_type != '':
				try:
					place = Place.objects.get(code=code)
					context = {

						'code': code,
						'bloock': block,
						'price': price,
						'radif': radif,
						'number': number,
						'floor': floor,
						'place_type': place_type,
						'latitude': latitude,
						'longitude': longitude,

						'error': True,
						'message': 'قبر با این کد وجود دارد.',
						'info': 'برای تصحیح قبر اینجا کلیک کنید.',
						'link': place

					}
					return render(request, 'admin-panel/new-place.html', context)
				except:
					try:
						Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
											 price=price,
											 latitude=latitude, longitude=longitude, status='Municipal',
											 type=place_type)
						message = 'قبر با کد ' + code + ' با موفقیت ثبت شد.'
						context = {

							'success': True,
							'message': message,
							'info': 'برای ویرایش اطلاعات وارد شده اینجا کلیک کنید.'

						}
						return render(request, 'admin-panel/new-place.html', context)
					except:
						context = {

							'code': code,
							'bloock': block,
							'price': price,
							'radif': radif,
							'number': number,
							'floor': floor,
							'place_type': place_type,
							'latitude': latitude,
							'longitude': longitude,

							'error': True,
							'message': 'اطلاعات وارد شده صحیح نمیباشد، لطفا دقت فرمایید.'
						}
						return render(request, 'admin-panel/new-place.html', context)
			else:
				context = {
					'error': True,
					'message': 'لطفا تمام اطلاعات مربوط به قبر را وارد کنید.',

					'code': code,
					'bloock': block,
					'price': price,
					'radif': radif,
					'number': number,
					'floor': floor,
					'place_type': place_type,
					'latitude': latitude,
					'longitude': longitude,

				}
				return render(request, 'admin-panel/new-place.html', context)

		context = {

		}

		return render(request, 'admin-panel/new-place.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/add-place/')


def Place_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		places = Place.objects.all()
		context = {
			'places': places,
		}
		return render(request, 'admin-panel/place-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/places-list/')


def Edit_Place(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		select_place = Place.objects.get(id=id)
		if request.method == 'POST':
			try:
				code = request.POST['code']
				block = request.POST['block']
				radif = request.POST['radif']
				price = request.POST['price']
				number = request.POST['number']
				floor = request.POST['floor']
				place_type = request.POST['place_type']
				latitude = request.POST['latitude']
				longitude = request.POST['longitude']
				if code != '' and block != '' and radif != '' and number != '' and floor != '' and place_type != '':
					try:
						select_place.code = code
						select_place.block = block
						select_place.radif = radif
						select_place.price = price
						select_place.number = number
						select_place.floor = floor
						select_place.type = place_type
						select_place.latitude = latitude
						select_place.longitude = longitude
						select_place.save()
						message = 'قبر با کد ' + code + ' با موفقیت ثبت شد.'
						context = {
							'success': True,
							'message': message,
							'info': 'برای تصحیح قبر اینجا کلیک کنید.',
							'select_place': select_place,
						}
						return render(request, 'admin-panel/edit-place-info.html', context)
					except:

						context = {

							'code': code,
							'bloock': block,
							'price': price,
							'radif': radif,
							'number': number,
							'floor': floor,
							'place_type': place_type,
							'latitude': latitude,
							'longitude': longitude,

							'error': True,
							'message': 'قبر با این کد وجود دارد.',

						}
						return render(request, 'admin-panel/new-place.html', context)
			except:
				try:
					price = request.POST['price']
					select_place.price = price
					select_place.save()
				except:
					pass
		context = {
			'select_place': select_place
		}
		return render(request, 'admin-panel/edit-place-info.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/edit-place-info/')


def Select_Deceased(request,id):
	if request.user.is_authenticated and request.user.is_staff:
		select_deceased = Deceased.objects.get(id=id)
		context = {
			'select_deceased':select_deceased
		}
		return render(request,'admin-panel/partial/select-deceased-base.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/select-deceased/'+id+'/')

def Sell_Service(request,id):
	if request.user.is_authenticated and request.user.is_staff:
		select_deceased = Deceased.objects.get(id = id)
		if request.method == 'POST':
			serves = request.POST.getlist('serves')
			str = ''
			for serve in serves:
				str +=serve
			str = str.split('Amir:D')
			last_buyer = request.POST['last_buyer']
			if last_buyer != 'Amir:D':
				buyer = Buyer.objects.get(pk=last_buyer)
			else:
				first_name = request.POST['first_name']
				last_name = request.POST['last_name']
				national_number = request.POST['national_number']
				phone_number = request.POST['phone_number']
				if first_name == '' and last_name == '' and phone_number== '':
					services = Service_List.objects.all()
					context = {
						'services': services,
						'error': True,
						'first_name': first_name,
						'last_name': last_name,
						'phone_number': phone_number,
						'national_number': national_number,
						'message': 'لطفا همه فیلد ها را پر کنید.',
						'select_deceased':select_deceased,

					}
					return render(request, 'admin-panel/add-service.html', context)

				if len(national_number) != 10:
					services = Service_List.objects.all()
					context = {
						'services': services,
						'error': True,
						'select_deceased':select_deceased,
						'first_name':first_name,
						'last_name':last_name,
						'phone_number':phone_number,
						'national_number':national_number,
						'message': 'کد ملی باید 10 رقمی باشد.'
					}
					return render(request, 'admin-panel/add-service.html', context)

				try:
					buyer = Buyer.objects.get(national_number=national_number)
				except:
					buyer = Buyer.objects.create(first_name=first_name,last_name=last_name,national_number=national_number,phone_number=phone_number)

			for i in str:
				if i=='':
					pass
				else:
					additional_service = Additional_Service.objects.create(status='PAID',buyer_id=buyer,service_id=Service_List.objects.get(pk=i),deceased_id=select_deceased)
					warnings = ['لطفا صفحه را رفرش نکنید، در غیر اینورت خدمات دوباره برای شما ثبت میشود!']
					message = 'خدمات  با موفقیت برای '+select_deceased.get_full_name()+' ثبت شد.'
					services = Service_List.objects.all()
					context = {
						'services':services,
						'warnings':warnings,
						'success':True,
						'message':message,
						'select_deceased': select_deceased

					}
					return render(request,'admin-panel/select-service-list.html',context)

		else:
			warnings = ['please be careful']
			buyers = Buyer.objects.filter(additional__deceased_id=select_deceased).distinct()
			services = Service_List.objects.all()
			context = {
				'warnings':warnings,
				'buyers':buyers,
				'services':services,
				'select_deceased':select_deceased
			}
			return render(request,'admin-panel/select-service-list.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/add-service/' + id + '/')


def Add_Service(request):
	if request.user.is_authenticated and request.user.is_staff:
		if request.method == 'POST':
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

		services = Service_List.objects.all()
		context = {
			'services':services
		}
		return render(request,'admin-panel/service-list.html',context)
	else:
		return redirect(request,'/Account/login/?next=/Admin/service-list/')

def Edit_Service(request,id):
	if request.user.is_authenticated and request.user.is_staff:
		select_service = Service_List.objects.get(id = id)
		if request.method == 'POST':
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


def Reserved_Services(request,id):
	if request.user.is_authenticated and request.user.is_staff:
		services = Additional_Service.objects.filter(deceased_id_id=id)
		select_deceased = Deceased.objects.get(pk=id)
		context = {
			'select_deceased':select_deceased,
			'services':services,
		}
		return render(request,'admin-panel/reserve-service-list.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/reserve-service/{}/'.format(str(id)))

def Add_New(request):
	if request.user.is_authenticated and request.user.is_staff:
		if request.method == 'POST':
			title = request.POST['title']
			context = request.POST['context']
			status = request.POST['status']
			if title != '' and context != '':
				new = New.objects.create(title=title, content=context, status=status)
				try:
					picture = request.FILES['picture']
					new.picture = picture
					new.save()
				except:
					pass
				message = 'خبر با عنوان <<' + new.title + '>> ایجاد شد.'
				context = {
					'success': True,
					'message': message,
					'info': 'برای ویرایش خبر اینجا کلیک کنید.',
					'new': new
				}
				return render(request, 'admin-panel/add_news.html', context)
			else:
				context = {
					'error': True,
					'message': 'لطفا اطلاعات مربوط به خبر جدید را وارد کنید.',

				}
				return render(request, 'admin-panel/add_news.html', context)
		context = {}
		return render(request, 'admin-panel/add_news.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/add-new/')


def News_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		news = New.objects.all()
		context = {
			'news': news
		}
		return render(request, 'admin-panel/news-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/news-list/')


def Edit_News(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		select_new = New.objects.get(id=id)
		if request.method == 'POST':
			title = request.POST['title']
			context = request.POST['context']
			status = request.POST['status']
			if title != '' and context != '':
				select_new.title = title
				select_new.content = context
				select_new.status = status
				select_new.save()
				try:
					picture = request.FILES['picture']
					select_new.picture = picture
					select_new.save()
				except:
					pass
				message = 'خبر با عنوان <<' + select_new.title + '>> ثبت شد.'
				context = {
					'success': True,
					'message': message,
					'info': 'برای بازگشت به لیست اخبار کلیک کنید.',
					'select_new': select_new
				}
				return render(request, 'admin-panel/edit-news-info.html', context)
			else:
				context = {
					'error': True,
					'message': 'لطفا هیچکدام از فیلد های "عنوان" و "جزئیات" را خالی نگذارید.',
					'select_new': select_new
				}
				return render(request, 'admin-panel/edit-news-info.html', context)
		context = {
			'select_new': select_new
		}
		return render(request, 'admin-panel/edit-news-info.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/edit-news-info/')
#
# def  Print_Deceased_info(request,id):
# 	from shahrdari import utils
# 	deceased = Deceased.objects.get(id=id)
# 	license = License.objects.get(deceased_id=deceased)
# 	death_certificate = Death_Certificate.objects.get(deceased_id=deceased)
# 	context = {
# 		'death':death_certificate,
# 		'license':license,
# 		'deceased':deceased
# 	}
#
# 	pdf = utils.render_to_pdf('admin-panel/forprint.html',context)
# 	return HttpResponse(pdf, content_type='application/pdf')

def Print_Deceased_info(request, id):
	select_deceased = Deceased.objects.get(pk=id)
	if request.user.is_authenticated and request.user.is_staff:
		select_license = License.objects.get(deceased_id=select_deceased)
		select_death_certificate = Death_Certificate.objects.get(deceased_id=select_deceased)
		context = {
			'select_deceased':select_deceased,
			'select_license':select_license,
			'select_death_certificate':select_death_certificate,
				   }
		return render(request,'admin-panel/forprint.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/print/{}/'.format(select_deceased.id))

def Add_Letter(request):
	if request.user.is_authenticated and request.user.is_staff:
		new = True
		if request.method == 'POST':
			code = request.POST['code']
			ckeditor = request.POST['ckeditor']
			try:
				letter = Archive.objects.create(code=code,description=ckeditor,status='Send')
				message = 'نامه شما با موفقیت ایجاد گردید.'
				context = {
					'new':True,
					'success': True,
					'message': message,
					'info': 'برای ویرایش نامه اینجا کلیک کنید.',
					'letter':letter

				}
				return render(request, 'admin-panel/editor.html', context=context)

			except:
				letter = Archive.objects.get(status='Send',code=code)
				message = 'نامه ای با کد وارد شده از قبل وجود دارد.'
				context={
					'new':new,
					'error':True,
					'message':message,
					'info':'برای ویرایش نامه اینجا کلیک کنید.',
					'letter':letter,
				}
				return render(request,'admin-panel/editor.html',context=context)

		warnings = ['لطفا از وارد کردن تصویر از طریق ckeditor تا اطلاع ثانوی خودداری کنید.']
		context = {
			'new':new,
			'warnings':warnings
		}
		return render(request,'admin-panel/editor.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/add-letter/')

def Inbox_Letter(request):
	if request.user.is_authenticated and request.user.is_staff:
		new = True
		if request.method == 'POST':
			code = request.POST['code']
			ckeditor = request.POST['ckeditor']
			try:
				picture = request.FILES['picture']
			except:
				picture = None
				context = {
					'error':True,
					'message':'هنگام وارد کردن تصویر مشکلی به وجود آمده است لطفا به پشتیبانی اعلام فرمایید.'
				}
				return render(request,'admin-panel/inbox-editor.html',context)

			try:
				letter = Archive.objects.create(code=code,description=ckeditor,status='Inbox',picture=picture)

				message = 'نامه شما با موفقیت ایجاد گردید.'
				context = {
					'select_letter':letter,
					'new':True,
					'success': True,
					'message': message,
					'info': 'برای ویرایش نامه اینجا کلیک کنید.',
					# 'letter':letter

				}
				return render(request, 'admin-panel/inbox-editor.html', context=context)

			except:
				letter = Archive.objects.get(status='Inbox',code=code)
				message = 'نامه ای با کد وارد شده از قبل وجود دارد.'
				context={
					'new':new,
					'error':True,
					'message':message,
					'info':'برای ویرایش نامه اینجا کلیک کنید.',
					'letter':letter,
				}
				return render(request,'admin-panel/inbox-editor.html',context=context)

		warnings = ['لطفا از وارد کردن تصویر از طریق ckeditor تا اطلاع ثانوی خودداری کنید.']
		context = {
			'new':new,
			'warnings':warnings
		}
		return render(request,'admin-panel/inbox-editor.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/inbox-letter/')


def Send_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		letters = Archive.objects.filter(status='Send')
		context = {
			'letters':letters
		}
		return render(request,'admin-panel/letter-list.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/send-list/')

def Receive_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		letters = Archive.objects.filter(status='Inbox')
		warnings = ['برای مشاهده تصویر و خلاصه نامه بروی کد آن کلیک کنید']
		context = {
			'warnings':warnings,
			'letters':letters
		}
		return render(request,'admin-panel/inbox-list.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/inbox-list/')


def Edit_Send_Letter(request,code_slug):
	if request.user.is_authenticated and request.user.is_staff:

		if request.method == 'POST':
			ckeditor = request.POST['ckeditor']
			select_letter = Archive.objects.get(code= code_slug)
			# return HttpResponse(select_letter)
			select_letter.description = ckeditor
			select_letter.save()
			context = {
				'select_letter':select_letter,
				'success':True,
				'message':'ویرایش با موفقیت انجام شد.'
			}
			return render(request, 'admin-panel/editor.html', context)
		select_letter = get_object_or_404(Archive,code=code_slug,status = 'Send')
		context = {
			'select_letter':select_letter,

		}
		return render(request,'admin-panel/editor.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/edit-send-letter/{}/'.format(code_slug))

def Edit_Receive_Letter(request,code_slug):
	if request.user.is_authenticated and request.user.is_staff:

		if request.method == 'POST':
			select_letter = Archive.objects.get(code= code_slug)
			ckeditor = request.POST['ckeditor']
			try:
				picture = request.FILES['picture']
				select_letter.picture = picture
			except:
				pass
			select_letter.description = ckeditor

			select_letter.save()
			context = {
				'select_letter':select_letter,
				'success':True,
				'message':'ویرایش با موفقیت انجام شد.'
			}
			return render(request, 'admin-panel/inbox-editor.html', context)
		select_letter = get_object_or_404(Archive,code=code_slug,status = 'Inbox')
		warnings = ['در صورت انتخاب نکردن تصویر، همان تصویر قبل ثبت میشود.']
		context = {
			'select_letter':select_letter,

		}
		return render(request,'admin-panel/inbox-editor.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/edit-inbox-letter/{}/'.format(code_slug))

def Add_Death_Cause(request):
	if request.user.is_authenticated and request.user.is_staff:
		if request.method == 'POST':
			title = request.POST['title']
			cause = Cause_Death.objects.create(name=title)
			message = 'علت مرگ با عنوان "{}" به موفقیت اضافه شد.'.format(cause.name)
			context = {
				'success':True,
				'message':message
			}
			return render(request,'admin-panel/add-cause-death.html',context)

		warnings = ['از اضافه کردن دلیل های مشابه و یک معنا خودداری کنید.']
		context = {
			'warnings':warnings,
		}
		return render(request,'admin-panel/add-cause-death.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/add-death-cause/')

def Death_Cause_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		death_causes = Cause_Death.objects.all()
		death_cers = Death_Certificate.objects.all()
		count_causes = {}
		for cause in death_causes:
			count_causes[cause.name] = Death_Certificate.objects.filter(cause_death_id__name=cause.name).count()

		context = {
			'count_causes':count_causes,
			'death_causes':death_causes,
			'death_cers':death_cers
		}
		return render(request,'admin-panel/death-cause-list.html',context)
	else:
		return redirect('/Account/login/?next=/Admin/death-cause-list/')


def Wait(request):
	return render(request,'amir.html',context={})