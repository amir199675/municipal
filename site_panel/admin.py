from django.contrib import admin
from .models import *
# Register your models here.


class DeceasedAdmin(admin.ModelAdmin):
	search_fields = ( 'first_name', 'last_name', 'national_number','muni_code')
	list_display = ('__str__','muni_code', 'national_number','presenter_id')
	ordering = ['-created']

	# filter_horizontal = ('first_name', 'last_name')
	fieldsets = (
		('اطلاعات اصلی', {
			'fields': ('first_name', 'last_name','national_number', 'muni_code')
		}),
		('دیگر اطلاعات', {
			'classes': ('wide'),
			'fields': ('identification_number','fa_name','mo_name','presenter_id','date_of_birth','place_of_birth','issue_date','bio','address'),
		}),
	)
	empty_value_display = '---------'

class LicenseAdmin(admin.ModelAdmin):
	search_fields = ('deceased_id__first_name','deceased_id__last_name', 'deceased_id__national_number','deceased_id__muni_code','move_status')
	list_display = ('__str__','document','deceased_national_number','move_status')
	ordering = ['-created']
	fieldsets = (
		('اطلاعات اصلی', {
			'fields': ( 'document','move_status', 'place_id','city_name','deceased_id')
		}),
		('دیگر اطلاعات', {
			'classes': ('wide'),
			'fields': ('license_status','picture','picture2','picture3'),
		}),
	)

	empty_value_display = '---------'

class DeathCertificateAdmin(admin.ModelAdmin):
	search_fields = (
	'deceased_id__first_name', 'deceased_id__last_name', 'deceased_id__national_number', 'deceased_id__muni_code')
	list_display = ('__str__','doctor','medical_system_number','death_certificate_number','deceased_national_number')
	ordering = ['-created']

	empty_value_display = '---------'

class PresenterAdmin(admin.ModelAdmin):
	search_fields = ('first_name','last_name','national_number','phone_number')
	list_display = (
	'__str__', 'national_number','phone_number')
	ordering = ['-created']

class BuyerAdmin(admin.ModelAdmin):
	search_fields = ('first_name','last_name','national_number','phone_number')
	list_display = (
	'__str__', 'national_number','phone_number')
	ordering = ['-created']

class PlaceAdmin(admin.ModelAdmin):
	search_fields = ('code', 'status','deceased_id__last_name', 'deceased_id__national_number', 'deceased_id__muni_code')
	list_display = (
		'__str__', 'status')
	ordering = ['-created']


admin.site.register(License,LicenseAdmin)
admin.site.register(Deceased,DeceasedAdmin)
admin.site.register(Death_Certificate,DeathCertificateAdmin)
admin.site.register(Presenter,PresenterAdmin)
admin.site.register(Madah)
admin.site.register(Marasem)
admin.site.register(Option)
admin.site.register(After_Death_Service)
admin.site.register(Memorial_Service)
admin.site.register(Reader_Service)
admin.site.register(Buyer,BuyerAdmin)
admin.site.register(Place,PlaceAdmin)
admin.site.register(Place_Service)
admin.site.register(Bill)
admin.site.register(Additional_Service)
admin.site.register(Archive)
admin.site.register(Cause_Death)
admin.site.register(Service_List)
admin.site.register(Driver)
admin.site.register(Car)
admin.site.register(Target)
admin.site.register(Movement_Service)
admin.site.register(Document)



