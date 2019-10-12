from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



app_name = 'Site_Panel'
urlpatterns = [

	path('Admin/',views.Index,name = 'index'),

	path('Admin/select-deceased/<id>/',views.Select_Deceased,name='select_deceased'),
	path('Admin/print/<id>/',views.Print_Deceased_info,name='print_deceased_info'),

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

	path('Admin/add-service/<id>/',views.Add_Service,name = 'add_service'),
	path('Admin/add-letter/',views.Add_Letter,name = 'add_letter'),



]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
