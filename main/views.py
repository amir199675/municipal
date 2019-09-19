from site_panel.models import *
from django.shortcuts import render, HttpResponse ,redirect
from .models import *
from datetime import datetime

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
