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
		warnings = ['از صحیح وارد شدن کد ملی اطمینان حاصل فرمایید','پس از وارد کردن متوفی لطفا جهت وارد کردن هزینه قبر آن اقدام نمایید.','اگر متوفی قبلا در سیستم ثبت شده است و قصد ویرایش اطلاعات دارید از طریق لیست متوفی اقدام کنید.']
		context = {
			'warnings':warnings,

		}
		return render(request, 'admin-panel/quick-deceased.html', context)

	else:
		return redirect('/Account/login/?next=/Admin/quick-new-deceased/')

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
