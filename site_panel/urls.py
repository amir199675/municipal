from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



app_name = 'Site_Panel'
urlpatterns = [

	path('',views.Index,name = 'index'),
	path('memorials/', views.Memorial, name = 'memorials'),
	path('Admin/quick-new-deceased/',views.Quick_Deceased,name = 'quick_new_deceased'),
	path('Admin/online-new-deceased/',views.Online_Deceased,name = 'online_new_deceased'),
	path('Admin/deceased-list/',views.Deceased_List,name = 'deceased_list'),


]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
