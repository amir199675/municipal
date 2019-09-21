from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



app_name = 'Site_Panel'
urlpatterns = [

	path('Admin/quick-new-deceased/',views.Quick_Deceased,name = 'quick_new_deceased'),
	path('Admin/online-new-deceased/',views.Online_Deceased,name = 'online_new_deceased'),
	path('Admin/deceased-list/',views.Deceased_List,name = 'deceased_list'),
	path('Admin/edit-deceased-info/<id>/',views.Edit_Deceased,name = 'edit-deceased-info'),

	path('Admin/add-place/',views.Add_Place,name = 'add_place'),
	path('Admin/places-list/',views.Place_List,name = 'places_list'),
	path('Admin/edit-place-info/<id>/',views.Edit_Place,name = 'edit-place-info'),

	path('Admin/add-news/',views.Add_New,name = 'add_news'),
	path('Admin/news-list/',views.News_List,name = 'news-list'),
	path('Admin/edit-news-info/<id>/',views.Edit_News,name = 'edit_news_info'),


]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
