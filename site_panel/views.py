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


def check_staff(user):
	return user.is_staff

def check_superuser(user):
	return user.is_superuser


def RandForPlaceServiceDocument():
	while (True):
		number = random.randint(100000, 999999)

		try:
			services = Place_Service.objects.get(document=number)
		except:
			return number


def Index(request):
	if request.user.is_authenticated and request.user.is_staff:
		# return HttpResponse(request.path)
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'صفحه اصلی پنل ادمین'
			seen.counter = int(seen.counter) + 1
			seen.save()

		context = {

		}
		return render(request, 'admin-panel/index.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/')


def Quick_Deceased(request):
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


		deceased = None

		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

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

			if first_name == '' or last_name == '':
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
			if national_number != '':
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

				deceased = Deceased.objects.create(national_number=national_number, first_name=first_name,
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
				place_service = Place_Service.objects.create(place_id=place, deceased_id=deceased,
															 document=RandForPlaceServiceDocument(),
															 payment_status='PAID')

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
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'اضافه کردن متوفی جدید'
			seen.counter = int(seen.counter) + 1
			seen.save()

		causes = Cause_Death.objects.all()
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

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
			place_of_death = request.POST['place_of_death']
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
				select_cause_death = Cause_Death.objects.get(id=cause_death)
			except:
				select_cause_death = None
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
					'muni_code': muni_code,
					'causes': causes,
					'place_of_death': place_of_death,
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
					'muni_code': muni_code,
					'causes': causes,
					'place_of_death': place_of_death,
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
					'muni_code': muni_code,
					'causes': causes,
					'place_of_death': place_of_death,
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
					'muni_code': muni_code,
					'causes': causes,
					'place_of_death': place_of_death,
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
							'muni_code': muni_code,
							'causes': causes,
							'place_of_death': place_of_death,
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
						try:
							place = Place.objects.create(code=code, block=block, radif=radif, number=number,
														 floor=floor,
														 type=place_type, longitude=longitude, latitude=latitude)
						except:
							return HttpResponse('خطا در ذخیره سازی قبر')
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
							'muni_code':muni_code,
							'causes':causes,
							'place_of_death':place_of_death,
							'error': True,
							'message': ' لطفا همه فیلد های مربوط به مشخصات محل دفن را پر کنید.',
						}
						return render(request, 'admin-panel/online-deceased.html', context)

			presenter = None
			try:
				buyer = Buyer.objects.get(national_number=presenter_national_number)
			except:
				try:
					buyer = Buyer.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
												 national_number=presenter_national_number,
												 identification_number=presenter_identification_number,
												 phone_number=presenter_phone_number)
				except:
					return HttpResponse('خطا در ذخیره سازی اطلاعات خریدار')

			try:
				presenter = Presenter.objects.get(national_number=presenter_national_number)
			except:
				try:
					presenter = Presenter.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
														 phone_number=presenter_phone_number,
														 national_number=presenter_national_number,
														 identification_number=presenter_identification_number,
														 address=presenter_address)
				except:
					return HttpResponse('خطا در ذخیره اطلاعات معرف')
				user = MyUser.objects.get(username=presenter_national_number)

			try:
				deceased = Deceased.objects.create(national_number=national_number, first_name=first_name,
												   last_name=last_name, fa_name=fa_name,
												   identification_number=identification_number, bio=bio,
												   date_of_birth=birth_day, address=address,
												   deceased_status=deceased_status, muni_code=muni_code,
												   place_of_birth=place_of_birth,
												   issue_date=issue_date, mo_name=mo_name, sex=sex)
			except:
				return HttpResponse('خطا در ذخیره سازی اطلاعات متوفی')
			deceased.presenter_id = presenter
			deceased.save()

			if place_save:
				place.save()

			if location:
				license = License.objects.get(deceased_id=deceased)
				license.move_status = 'SEND-OUT'
				license.city_name = location
				license.picture = picture
				try:
					presenter_document_one = request.FILES['presenter_document_one']
					license.picture2 = presenter_document_one
				except:
					pass
				try:
					presenter_document_two = request.FILES['presenter_document_two']
					license.picture3 = presenter_document_two
				except:
					pass
				license.license_status = license_status

				license.save()
			else:

				license = License.objects.get(deceased_id=deceased)
				license.move_status = 'FERDOS-REZA'
				license.place_id = place
				license.picture = picture
				try:
					presenter_document_one = request.FILES['presenter_document_one']
					license.picture2 = presenter_document_one
				except:
					pass
				try:
					presenter_document_two = request.FILES['presenter_document_two']
					license.picture3 = presenter_document_two
				except:
					pass
				license.license_status = license_status
				license.save()
				try:
					buyer = Buyer.objects.get(national_number=presenter_national_number)
				except:
					try:
						buyer = Buyer.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
													 national_number=presenter_national_number,
													 identification_number=presenter_identification_number,
													 phone_number=presenter_phone_number)
					except:
						return HttpResponse('خطا در ذخیره سازی اطلاعات خریدار')
				if license_status == 'CONFIRMED':
					try:
						place_service = Place_Service.objects.create(buyer_id=buyer, place_id=place,
																	 deceased_id=deceased,
																	 document=RandForPlaceServiceDocument(),
																	 payment_status='PAID')
					except:

						return HttpResponse('خطا در ذخیره سازی اطلاعات رزرو قبر')
				else:
					pass

			death_certificate = Death_Certificate.objects.get(deceased_id=deceased)
			death_certificate.doctor_first_name = doctor_first_name
			death_certificate.doctor_last_name = doctor_last_name
			death_certificate.medical_system_number = medical_system_number
			death_certificate.death_certificate_number = death_certificate_number
			death_certificate.date_of_death = date_of_death
			death_certificate.cause_death_id = select_cause_death
			death_certificate.date_of_death = date_of_death
			death_certificate.status = death_certificate_stats
			death_certificate.place = place_of_death
			death_certificate.save()
			message = 'متوفی ' + deceased.get_full_name() + ' با موفقیت ثبت شد'
			causes = Cause_Death.objects.all()

			context = {
				'success': True,
				'message': message,
				'causes': causes,
				'info': 'برای ویرایش اطلاعات وارد شده اینجا کلیک کنید.',
				'deceased': deceased,

			}
			return render(request, 'admin-panel/online-deceased.html', context)
		warnings = ['لطفا همه موارد ستاره دار را با دقت پر کنید.',
					'پس از وارد کردن متوفی لطفا جهت وارد کردن هزینه قبر آن اقدام نمایید.',
					'اگر متوفی قبلا در سیستم ثبت شده است و قصد ویرایش اطلاعات دارید از طریق لیست متوفی اقدام کنید.']

		context = {
			'causes': causes,
			'warnings': warnings,

		}
		return render(request, 'admin-panel/online-deceased.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/online-new-deceased/')


def Deceased_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'لیست متوفی'
			seen.counter = int(seen.counter) + 1
			seen.save()

		deceaseds = Deceased.objects.all()
		warnings = ['برای مشاهده جزییات محل دفن بروی کد قبر کلیک کنید.']
		context = {

			'deceaseds': deceaseds,
			'warnings': warnings,
		}

		return render(request, 'admin-panel/deceased-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/deceased-list/')


def Edit_Deceased(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'ویرایش مشخصات متوفی'
			seen.counter = int(seen.counter) + 1
			seen.save()

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

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

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
			place_of_death = request.POST['place_of_death']
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
									'causes': causes,
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

			if first_name == '' or last_name == '':
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

					if len(national_number) != 10:
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
							presenter = Presenter.objects.create(first_name=presenter_first_name,
																 last_name=presenter_last_name,
																 national_number=presenter_national_number,
																 identification_number=presenter_identification_number
																 , phone_number=presenter_phone_number,
																 address=presenter_address)

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
						context = {
							'causes': causes,
							'select_deceased': select_deceased,
							'certificate': certificate,
							'license': license,
							'error': True,
							'message': 'لطفا همه اطلاعات مربوط به متوفی را وارد کنید!'
						}
						return render(request, 'admin-panel/edit-deceased-info.html', context)
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
				if pic:
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
			certificate.place = place_of_death
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
		return redirect('/Account/login/?next=/Admin/edit-deceased-info/' + id)


def Add_Place(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'اضافه کردن قبر'
			seen.counter = int(seen.counter) + 1
			seen.save()
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

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
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'لیست قبور'
			seen.counter = int(seen.counter) + 1
			seen.save()
		places = Place.objects.all()
		context = {
			'places': places,
		}
		return render(request, 'admin-panel/place-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/places-list/')


def Edit_Place(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'ویرایش قبر'
			seen.counter = int(seen.counter) + 1
			seen.save()
		select_place = Place.objects.get(id=id)
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

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


def Select_Deceased(request, id):

	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'انتخاب متوفی'
			seen.counter = int(seen.counter) + 1
			seen.save()

		select_deceased = Deceased.objects.get(id=id)
		context = {
			'select_deceased': select_deceased
		}
		return render(request, 'admin-panel/partial/select-deceased-base.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/select-deceased/' + id + '/')


def Add_New(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'اضافه کردن خبر'
			seen.counter = int(seen.counter) + 1
			seen.save()
		if request.method == 'POST':
			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

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

		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'لیست اخبار'
			seen.counter = int(seen.counter) + 1
			seen.save()
		news = New.objects.all()
		context = {
			'news': news
		}
		return render(request, 'admin-panel/news-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/news-list/')


def Edit_News(request, id):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'ویرایش خبر'
			seen.counter = int(seen.counter) + 1
			seen.save()
		select_new = New.objects.get(id=id)
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

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
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'پرینت اطلاعات متوفی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		select_license = License.objects.get(deceased_id=select_deceased)
		select_death_certificate = Death_Certificate.objects.get(deceased_id=select_deceased)
		context = {
			'select_deceased': select_deceased,
			'select_license': select_license,
			'select_death_certificate': select_death_certificate,
		}
		return render(request, 'admin-panel/forprint.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/print/{}/'.format(select_deceased.id))


def Add_Letter(request):
	if request.user.is_authenticated and request.user.is_staff:

		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'اضافه کردن خروجی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		new = True
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			code = request.POST['code']
			ckeditor = request.POST['ckeditor']
			try:
				select_letter = Archive.objects.create(code=code, description=ckeditor, status='Send')
				message = 'نامه شما با موفقیت ایجاد گردید.'
				context = {
					'new': True,
					'success': True,
					'message': message,
					'info': 'برای ویرایش نامه اینجا کلیک کنید.',
					'select_letter': select_letter

				}
				return render(request, 'admin-panel/editor.html', context=context)

			except:
				letter = Archive.objects.get(status='Send', code=code)
				message = 'نامه ای با کد وارد شده از قبل وجود دارد.'
				context = {
					'new': new,
					'error': True,
					'message': message,
					'info': 'برای ویرایش نامه اینجا کلیک کنید.',
					'letter': letter,
				}
				return render(request, 'admin-panel/editor.html', context=context)

		warnings = ['لطفا از وارد کردن تصویر از طریق ckeditor تا اطلاع ثانوی خودداری کنید.']
		context = {
			'new': new,
			'warnings': warnings
		}
		return render(request, 'admin-panel/editor.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/add-letter/')


def Inbox_Letter(request):
	if request.user.is_authenticated and request.user.is_staff:

		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'ایجاد نامه ورودی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		new = True
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			code = request.POST['code']
			ckeditor = request.POST['ckeditor']
			try:
				picture = request.FILES['picture']
			except:
				picture = None
				context = {
					'error': True,
					'message': 'هنگام وارد کردن تصویر مشکلی به وجود آمده است لطفا به پشتیبانی اعلام فرمایید.'
				}
				return render(request, 'admin-panel/inbox-editor.html', context)

			try:
				letter = Archive.objects.create(code=code, description=ckeditor, status='Inbox', picture=picture)

				message = 'نامه شما با موفقیت ایجاد گردید.'
				context = {
					'select_letter': letter,
					'new': True,
					'success': True,
					'message': message,
					'info': 'برای ویرایش نامه اینجا کلیک کنید.',
					# 'letter':letter

				}
				return render(request, 'admin-panel/inbox-editor.html', context=context)

			except:
				letter = Archive.objects.get(status='Inbox', code=code)
				message = 'نامه ای با کد وارد شده از قبل وجود دارد.'
				context = {
					'new': new,
					'error': True,
					'message': message,
					'info': 'برای ویرایش نامه اینجا کلیک کنید.',
					'letter': letter,
				}
				return render(request, 'admin-panel/inbox-editor.html', context=context)

		warnings = ['لطفا از وارد کردن تصویر از طریق ckeditor تا اطلاع ثانوی خودداری کنید.']
		context = {
			'new': new,
			'warnings': warnings
		}
		return render(request, 'admin-panel/inbox-editor.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/inbox-letter/')


def Send_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'لیست نامه های خروجی'
			seen.counter = int(seen.counter) + 1
			seen.save()

		letters = Archive.objects.filter(status='Send')
		context = {
			'letters': letters
		}
		return render(request, 'admin-panel/letter-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/send-list/')


def Receive_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'لیست نامه های ورودی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		letters = Archive.objects.filter(status='Inbox')
		warnings = ['برای مشاهده تصویر و خلاصه نامه بروی کد آن کلیک کنید']
		context = {
			'warnings': warnings,
			'letters': letters
		}
		return render(request, 'admin-panel/inbox-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/inbox-list/')


def Edit_Send_Letter(request, code_slug):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'ویرایش نامه خروجی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			ckeditor = request.POST['ckeditor']
			select_letter = Archive.objects.get(code=code_slug)
			# return HttpResponse(select_letter)
			select_letter.description = ckeditor
			select_letter.save()
			context = {
				'select_letter': select_letter,
				'success': True,
				'message': 'ویرایش با موفقیت انجام شد.'
			}
			return render(request, 'admin-panel/editor.html', context)
		select_letter = get_object_or_404(Archive, id=code_slug, status='Send')
		context = {
			'select_letter': select_letter,

		}
		return render(request, 'admin-panel/editor.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/edit-send-letter/{}/'.format(code_slug))


def Edit_Receive_Letter(request, code_slug):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'ویرایش نامه ورودی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			select_letter = Archive.objects.get(code=code_slug)
			ckeditor = request.POST['ckeditor']
			try:
				picture = request.FILES['picture']
				select_letter.picture = picture
			except:
				pass
			select_letter.description = ckeditor

			select_letter.save()
			context = {
				'select_letter': select_letter,
				'success': True,
				'message': 'ویرایش با موفقیت انجام شد.'
			}
			return render(request, 'admin-panel/inbox-editor.html', context)
		select_letter = get_object_or_404(Archive, code=code_slug, status='Inbox')
		warnings = ['در صورت انتخاب نکردن تصویر، همان تصویر قبل ثبت میشود.']
		context = {
			'select_letter': select_letter,

		}
		return render(request, 'admin-panel/inbox-editor.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/edit-inbox-letter/{}/'.format(code_slug))


def Add_Death_Cause(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'اضافه کردن علت مرگ'
			seen.counter = int(seen.counter) + 1
			seen.save()
		if request.method == 'POST':

			groups = request.user.groups.all()
			for group in groups:
				if group.name == 'viewer':
					return HttpResponse('شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

			title = request.POST['title']
			cause = Cause_Death.objects.create(name=title)
			message = 'علت مرگ با عنوان "{}" به موفقیت اضافه شد.'.format(cause.name)
			context = {
				'success': True,
				'message': message
			}
			return render(request, 'admin-panel/add-cause-death.html', context)

		warnings = ['از اضافه کردن دلیل های مشابه و یک معنا خودداری کنید.']
		context = {
			'warnings': warnings,
		}
		return render(request, 'admin-panel/add-cause-death.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/add-death-cause/')


def Death_Cause_List(request):
	if request.user.is_authenticated and request.user.is_staff:
		try:
			seen = Counter_Seen.objects.get(user_id=request.user,path=request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user,path=request.path)
			seen.name = 'لیست علت مرگ'
			seen.counter = int(seen.counter) + 1
			seen.save()
		death_causes = Cause_Death.objects.all()
		death_cers = Death_Certificate.objects.all()
		count_causes = {}
		for cause in death_causes:
			count_causes[cause.name] = Death_Certificate.objects.filter(cause_death_id__name=cause.name).count()

		context = {
			'count_causes': count_causes,
			'death_causes': death_causes,
			'death_cers': death_cers
		}
		return render(request, 'admin-panel/death-cause-list.html', context)
	else:
		return redirect('/Account/login/?next=/Admin/death-cause-list/')


#
# def Print_Movement_Cert(request, id):
# 	if request.user.is_authenticated and request.user.is_staff:
# 		select_deceased = Deceased.objects.get(id=id)
# 		select_death_cert = Death_Certificate.objects.get(deceased_id=select_deceased)
# 		movement_cert = Movement_Certificate.objects.get(license_id__deceased_id=select_deceased)
# 		select_license = License.objects.get(deceased_id=select_deceased)
# 		if movement_cert.status == 'confirmation':
# 			context = {
# 				'select_death_cert': select_death_cert,
# 				'select_deceased': select_deceased,
# 				'select_license': select_license,
#
# 			}
# 			return render(request, 'admin-panel/movement/movement_cert_print.html', context)
# 	else:
#
# 		return redirect('/Account/login/?next=/Admin/movement_certificate_print/{}'.format(id))



@user_passes_test(check_staff)
def Census_Deceased(request):
	if request.method == 'POST':
		try:
			seen = Counter_Seen.objects.get(user_id=request.user, path= request.path)
			seen.counter = int(seen.counter) + 1
			seen.save()
		except:
			# return HttpResponse(request.user)
			seen = Counter_Seen.objects.create(user_id=request.user, path= request.path)
			seen.name = 'آمارگیری متوفی'
			seen.counter = int(seen.counter) + 1
			seen.save()
		groups = request.user.groups.all()
		for group in groups:
			if group.name == 'viewer':
				return HttpResponse(
					'شما اجازه فیلترینگ و یا اضافه کردن یا هرگونه تغییرات را ندارید.در صورت اعتراض لطفا با برنامه نویس سایت هماهنگ کنید با تشکر!')

		sex = request.POST['sex']
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
			date_s = True
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
			date_e = True
			end_date = datetime.now().date()

		# return HttpResponse(sex)
		try:
			license_id = request.POST['city']
		except:
			license_id = 'all'
		if license_id != 'all':
			try:
				license = License.objects.get(id=license_id)
				city = license.city_name
				status = 'SEND-OUT'
			except:
				city = ''
				status = ''
		else:
			city = ''
			status = ''

		try:
			cause_death_id = request.POST['cause_death']
		except:
			cause_death_id = 'all'
		if cause_death_id != 'all' :
			try:
				cause_death = Cause_Death.objects.get(id = cause_death_id)
				cause_death = cause_death.name
			except:
				cause_death = ''
		else:
			cause_death = 'all'
		if status == 'SEND-OUT':
			if date_s and date_e :

				if cause_death == 'all':

					deceaseds = Deceased.objects.filter(sex=sex,license__city_name__contains=city,certificate__date_of_death__gte=start_date,certificate__date_of_death__lte=end_date)
				else:
					deceaseds = Deceased.objects.filter(sex=sex,license__city_name__contains=city,certificate__cause_death_id__name__contains=cause_death,certificate__date_of_death__gte=start_date,certificate__date_of_death__lte=end_date)
			else:
				if cause_death == 'all':
					deceaseds = Deceased.objects.filter(sex=sex,license__city_name__contains=city)
				else:
					deceaseds = Deceased.objects.filter(sex=sex,license__city_name__contains=city,
														certificate__cause_death_id__name__contains=cause_death,
														certificate__date_of_death__gte=start_date,
														certificate__date_of_death__lte=end_date)

		else:
			if date_e and date_s :

				if cause_death == 'all':
					deceaseds = Deceased.objects.filter(sex=sex)
				else:
					deceaseds = Deceased.objects.filter(sex=sex,certificate__cause_death_id__name__contains=cause_death)
			else:
				if cause_death == 'all':
					deceaseds = Deceased.objects.filter(sex=sex,certificate__date_of_death__gte=start_date,certificate__date_of_death__lte=end_date)
				else:
					deceaseds = Deceased.objects.filter(sex=sex,certificate__cause_death_id__name__contains=cause_death,certificate__date_of_death__gte=start_date,certificate__date_of_death__lte=end_date)

		causes = Cause_Death.objects.all()
		licenses = License.objects.filter(city_name__isnull=False).distinct('city_name')
		select_cause = cause_death
		select_city = city
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
		if deceaseds.count() == 0 :
			error = True

		context = {
			'sex':sex,
			'error':error,
			'select_start':select_start,
			'select_end':select_end,
			'select_cause':select_cause,
			'select_city':select_city,
			'causes': causes,
			'licenses': licenses,
			'deceaseds':deceaseds
		}
		return render(request,'admin-panel/deceased_census.html',context)

	causes = Cause_Death.objects.all()
	licenses = License.objects.filter(city_name__isnull=False).distinct('city_name')
	context = {
		'causes':causes,
		'licenses':licenses,

	}
	return render(request, 'admin-panel/deceased_census.html', context)


def Wait(request):
	return render(request, 'amir.html', context={})

@user_passes_test(check_superuser)
def Seens(request):
	seens = Counter_Seen.objects.all()
	context = {
		'seens':seens
	}
	return render(request,'admin-panel/superuser/seen-list.html',context)