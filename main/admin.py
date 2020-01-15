from django.contrib import admin
from .models import *
# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
	search_fields = ('national_number', 'phone_number','first_name','last_name','is_staff')
	list_display= ('__str__', 'national_number', 'phone_number','is_staff')

admin.site.register(New)
admin.site.register(Hadith)
admin.site.register(Slider)
admin.site.register(MyUser,MyUserAdmin)
admin.site.register(Message)

