from django.shortcuts import render, HttpResponse
from main.models import *
from .models import *
from datetime import datetime


def Quick_Deceased(request):
	if request.method == 'POST':

		presenter_first_name = request.POST['presenter_first_name']
		presenter_last_name = request.POST['presenter_last_name']
		presenter_phone_number = request.POST['presenter_phone_number']
		presenter_national_number = request.POST['presenter_national_number']
		presenter_identification_number = request.POST['presenter_identification_number']
		presenter = None
		try:
			presenter = Presenter.objects.get(national_number=presenter_national_number)
		except:
			presenter = Presenter.objects.create(first_name=presenter_first_name, last_name=presenter_last_name,
												 phone_number=presenter_phone_number,
												 national_number=presenter_national_number,
												 identification_number=presenter_identification_number)

		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		fa_name = request.POST['fa_name']
		identification_number = request.POST['identification_number']
		national_number = request.POST['national_number']
		bio = request.POST['bio']

		if national_number == '':
			context = {}
			return render(request, '', context)
		deceased = None
		try:
			deceased = Deceased.objects.get(national_number=national_number)
			context = {}
			return render(request, '', context)
		except:
			deceased = Deceased.objects.create(national_number=national_number, first_name=first_name,
											   last_name=last_name, fa_name=fa_name,
											   identification_number=identification_number, bio=bio)
			deceased.presenter_id = presenter
			deceased.save()

		code = request.POST['code']
		block = request.POST['block']
		radif = request.POST['radif']
		number = request.POST['number']
		floor = request.POST['floor']
		place_type = request.POST['place_type']
		place = None
		try:
			place = Place.objects.get(code=code)
		except:
			place = Place.objects.create(code=code, block=block, radif=radif, number=number, floor=floor,
										 type=place_type)

		license = License.objects.get(deceased_id=deceased)
		license.place_id = place
		license.status = 'CONFIRMED'

		doctor_first_name = request.POST['doctor_first_name']
		doctor_last_name = request.POST['doctor_last_name']
		medical_system_number = request.POST['medical_system_number']
		death_certificate_number = request.POST['death_certificate_number']
		date_of_death = request.POST['date_of_death']
		cause_death = request.POST['cause_death']
		date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d')

		death_certificate = Death_Certificate.objects.get(deceased_id=deceased)
		death_certificate.doctor_first_name = doctor_first_name
		death_certificate.doctor_last_name=doctor_last_name
		death_certificate.medical_system_number=medical_system_number
		death_certificate.death_certificate_number=death_certificate_number
		death_certificate.date_of_death=date_of_death
		death_certificate.cause_death=cause_death
		death_certificate.date_of_death =date_of_death
		death_certificate.save()


	context = {}
	return render(request, 'admin-panel/quick-deceased.html', context)


def amir(request):
	if request.method == 'POST':
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		deceased_status = request.POST['deceased_status']
		deceased_type = request.POST['deceased_type']
		date_of_birth = request.POST['date_of_birth']
		date_of_death = request.POST['date_of_death']
		sex = request.POST['sex']
		mo_name = request.POST['mo_name']
		place_of_birth = request.POST['place_of_birth']
		issue_date = request.POST['issue_date']
		address = request.POST['address']
		code = request.POST['code']
		longitude = request.POST['longitude']
		latitude = request.POST['latitude']
		price = request.POST['price']
		radif = request.POST['radif']
		ghete = request.POST['ghete']
		block = request.POST['block']
		number = request.POST['number']
		floor = request.POST['floor']
		status = request.POST['status']
		type = request.POST['type']
		date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
		date_of_death = datetime.strptime(date_of_death, '%Y-%m-%d')
		try:
			place = Place.objects.get(code=code, number=number, ghete=ghete, floor=floor, radif=radif, block=block)
			place.status = 'Sold'
			place.save()
		except:
			place = Place.objects.create(code=code,
										 number=number, ghete=ghete, floor=floor, radif=radif, block=block,
										 status='Sold', type=type)
		dec = Deceased.objects.create(deceased_type=deceased_type, name=name, deceased_status=deceased_status,
									  national_number=national_number, date_of_birth=date_of_birth, sex=sex,
									  fa_name=fa_name, mo_name=mo_name, identification_number=identification_number)
		license = License.objects.get(deceased_id=dec)
		license.place_id = place
		license.status = 'CONFIRMED'
		license.save()

	return render(request, 'main-site/test.html', context={})


def Index(request):
	place_count = Place.objects.all().count()
	news = New.objects.all()[:5]
	ahadith = Hadith.objects.all()
	sliders = Slider.objects.filter(status='Active')
	context = {
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
