from django.shortcuts import render

from rest_framework.views import *
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import generics

from datetime import datetime , timedelta

from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


# Create your views here.

class APIListMadah(APIView):
	def get(self, request, *args, **kwargs):
		madahan = Madah.objects.all()
		serializer = ChanterSerializer(madahan,many=True)
		return Response(serializer.data)


class APIListPlace(APIView):
	def get(self,request,*args,**kwargs):
		places = Place.objects.all()
		serializer = PlaceSerializers(places,many=True)
		return Response(serializer.data)

class APIListDeceased(APIView):
	def get(self,*args,**kwargs):
		deceased = Deceased.objects.all()
		serializer = DeceasedSerializer(deceased,many=True)
		return Response(serializer.data)


class DeceasedAdvanceSearchAPIView(generics.ListAPIView):
	serializer_class = DeceasedSerializer

	def get_queryset(self):
		queryset = Deceased.objects.all()
		first_name = self.request.query_params.get('name','')
		last_name = self.request.query_params.get('last_name','')
		ghete = self.request.query_params.get('ghete','')
		block = self.request.query_params.get('block','')
		fa_name = self.request.query_params.get('father_name','')

		date_start = self.request.query_params.get('date_start' , '')
		date_end = self.request.query_params.get('date_end','')



		if date_start:
			date_start = datetime.strptime(date_start,'%Y-%m-%d')
		else:
			date_start = datetime.now() - timedelta(weeks=5200)
			date_start = date_start.date()



		if date_end:
			date_end = datetime.strptime(date_end,'%Y-%m-%d')
		else:
			date_end = datetime.now().date()
		return queryset.filter(date_of_death__lte=date_end,date_of_death__gte=date_start,first_name__contains=first_name,fa_name__contains=fa_name ,last_name__contains=last_name,place_id__ghete__contains=ghete,place_id__block__contains=block)




class DeceasedSimpleSearchAPIView(generics.ListAPIView):
	serializer_class = DeceasedSerializer
	queryset = Deceased.objects.all()
	filter_backends = (DjangoFilterBackend,SearchFilter)
	search_fields = ('first_name','last_name'	)





class After_DeathCreateAPIView(APIView):
	# queryset = After_Death.objects.all() #generic.CreateAPIView
	# serializer_class = After_DeathSerializer
	def get(self, request, *args, **kwargs):
		afters = After_Death_Service.objects.all()
		serializer = After_DeathSerializer(afters,many=True)
		return Response(serializer.data)

	def post(self,request,*args,**kwargs):
		start_time = request.data.get('start_time','')
		start_time = datetime.strptime(start_time,'%Y-%m-%dT%H:%M:%fZ')
		legal_time = datetime.now() + timedelta(days=3)
		other_option = request.data.get('option_id','')
		deceased = request.data.get('deceased_id','')
		user = request.data.get('user_id','')

		deceased_id  = Deceased.objects.get(pk=deceased)
		user_id = User.objects.get(id=user)
		if start_time < legal_time:
			payload= {
				"message":"زمان باید حداقل سه روز بعد باشد"
			}
			return Response(payload,status= status.HTTP_404_NOT_FOUND)
		After_Death_Service.objects.create(deceased_id=deceased_id,user_id=user_id,start_time=start_time)
		after = After_Death_Service.objects.get(deceased_id=deceased_id,user_id=user_id,start_time=start_time)

		for value in other_option:
			option = Option.objects.get(id=value)
			after.other_option_id.add(option)
			after.save()
		serializer = After_DeathSerializer(after)
		return Response(serializer.data,status=status.HTTP_201_CREATED)



class After_Death_GetAPIView(APIView):
	def get(self,request,*args,**kwargs):
		afters = After_Death_Service.objects.all()
		serializer = After_DeathSerializer(afters, many=True)
		return Response(serializer.data)

	def post(self,request,*args,**kwargs):
		deceased_id= request.data.get('deceased_id','')
		afters = After_Death_Service.objects.filter(deceased_id__id=deceased_id)
		serializer = After_DeathSerializer(afters , many=True)
		return Response(serializer.data, status=status.HTTP_201_CREATED)