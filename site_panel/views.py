from django.shortcuts import render , HttpResponse
from main.models import *
from .models import *
from datetime import datetime


def New_Deceased(request):
	context = {}
	return render(request,'admin-panel/new-deceased.html',context)

def amir(request):
	if request.method == 'POST':
		name = request.POST['name']
		deceased_status = request.POST['deceased_status']
		deceased_type = request.POST['deceased_type']
		national_number = request.POST['national_number']
		date_of_birth = request.POST['date_of_birth']
		date_of_death = request.POST['date_of_death']
		sex = request.POST['sex']
		fa_name = request.POST['fa_name']
		mo_name = request.POST['mo_name']
		bio = request.POST['bio']
		identification_number = request.POST['identification_number']
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
		date_of_birth = datetime.strptime(date_of_birth,'%Y-%m-%d')
		date_of_death = datetime.strptime(date_of_death,'%Y-%m-%d')
		try:
			place = Place.objects.get(code=code,number=number,ghete=ghete,floor=floor,radif=radif,block=block)
			place.status = 'Sold'
			place.save()
		except:
			place = Place.objects.create(code=code,
										 number=number,ghete=ghete, floor=floor, radif=radif, block=block, status='Sold', type=type)
		dec = Deceased.objects.create(deceased_type=deceased_type,name=name,deceased_status=deceased_status,national_number=national_number,date_of_birth=date_of_birth,sex=sex,fa_name=fa_name,mo_name=mo_name,identification_number=identification_number)
		license = License.objects.get(deceased_id=dec)
		license.place_id = place
		license.status = 'CONFIRMED'
		license.save()

	return render(request,'main-site/test.html',context={})

def Index (request):

	place_count = Place.objects.all().count()
	news = New.objects.all()[:5]
	ahadith = Hadith.objects.all()
	sliders = Slider.objects.filter(status='Active')
	context = {
		'sliders':sliders,
		'ahadith':ahadith,
		'news':news,
		'place_count':place_count,
	}
	return render(request, 'main-site/index.html', context)

def Memorial (request):

	marasems = Marasem.objects.all()
	context = {
		'marasems':marasems,
		'black':True
	}
	return render(request,'main-site/memorial.html',context)