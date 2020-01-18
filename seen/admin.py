from django.contrib import admin
from .models import *
# Register your models here.
class CounterSeenAdmin(admin.ModelAdmin):
	list_display = ('__str__','counter','updated')
	list_editable = ('counter',)

admin.site.register(Counter_Seen,CounterSeenAdmin)
admin.site.register(Last_Seen,CounterSeenAdmin)
