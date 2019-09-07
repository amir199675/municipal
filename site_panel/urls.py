from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



app_name = 'Site_Panel'
urlpatterns = [

	path('',views.Index,name = 'index'),
	path('memorials/', views.Memorial, name = 'memorials'),
	path('amir/', views.amir, name = 'amir'),
	path('Admin/new-deceased/',views.New_Deceased,name = 'new_deceased')

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
