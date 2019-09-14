from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.models import User
from site_panel.models import *

class ChanterSerializer(ModelSerializer):
	class Meta:
		model = Madah
		fields = ('id','name','phone_number','grade')


class PlaceSerializers(ModelSerializer):
	class Meta:
		model = Place
		fields = '__all__'



class DeceasedSerializer(ModelSerializer):

	class PlaceSerializer(ModelSerializer):
		class Meta:
			model = Place
			fields = '__all__'

	place_id = PlaceSerializer(read_only=True)
	class Meta:
		model = Deceased
		fields = '__all__'

class Deceased_Search(ModelSerializer):
	class Meta :
		model = Deceased
		fields = ('first_name',)




class After_DeathSerializer(ModelSerializer):
	class MarasemSerializer(ModelSerializer):
		class Meta:
			model = Marasem
			fields = '__all__'

	class MadahSerializer(ModelSerializer):
		class Meta:
			model = Madah
			fields = '__all__'

	class Other_OptionSerializer(ModelSerializer):
		class Meta:
			model = Option
			fields = '__all__'

	class UserSerializer(ModelSerializer):
		class Meta:
			model = User
			fields = '__all__'
	class DeceasedSerializer(ModelSerializer):
		class Meta:
			model = Deceased
			fields = '__all__'

	deceased_id = DeceasedSerializer(read_only=True)
	option_id = Other_OptionSerializer(read_only=True,many=True)
	madah_id = MadahSerializer(read_only=True)
	marasem_id = MarasemSerializer(read_only=True)
	user_id = UserSerializer(read_only=True)
	class Meta :
		model = After_Death_Service
		fields = '__all__'



class LicenseSerializer(ModelSerializer):
	class DeceasedSerializer(ModelSerializer):
		class Meta:
			model = Deceased
			fields = '__all__'

	class PlaceSerializer(ModelSerializer):
		class Meta:
			model = Place
			fields = '__all__'

	deceased_id = DeceasedSerializer(read_only=True)
	place_id = PlaceSerializers(read_only=True)

	class Meta:
		model = License
		fields = '__all__'