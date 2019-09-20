from site_panel.models import *
from django.shortcuts import render, HttpResponse ,redirect
from .models import *
from datetime import datetime

def Index(request):
	place_count = Place.objects.all().count()
	ferdos_deceased_count = License.objects.filter(move_status='FERDOS-REZA').count()
	out_deceased_count = License.objects.filter(move_status='SEND-OUT').count()
	users_count = MyUser.objects.all().count()
	news = New.objects.all()[:5]
	ahadith = Hadith.objects.all()
	sliders = Slider.objects.filter(status='Active')
	black = False
	if sliders.count() == 0:
		black = True
	context = {
		'users_count':users_count,
		'ferdos_deceased_count':ferdos_deceased_count,
		'out_deceased_count':out_deceased_count,
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
