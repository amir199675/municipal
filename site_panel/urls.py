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

	path('Admin/reserve-service/<id>/',views.Sell_Service,name = 'sell_service'),
	path('Admin/add-service/',views.Add_Service,name = 'add_service'),
	path('Admin/service-list/',views.Services,name = 'service-list'),
	path('Admin/service-list/edit/<id>/',views.Edit_Service,name = 'edit_service'),
	path('Admin/reserved-service-list/<id>/',views.Reserved_Services,name = 'reserve-service'),

	path('Admin/add-letter/',views.Add_Letter,name = 'add_letter'),
	path('Admin/inbox-letter/',views.Inbox_Letter,name = 'inbox_letter'),
	path('Admin/send-list/',views.Send_List,name = 'send_list'),
	path('Admin/inbox-list/',views.Receive_List,name = 'inbox_list'),
	path('Admin/edit-send-letter/<code_slug>/',views.Edit_Send_Letter,name = 'edit_send_letter'),
	path('Admin/edit-receive-letter/<code_slug>/',views.Edit_Receive_Letter,name = 'edit_receive_letter'),

	path('Admin/add-death-cause/',views.Add_Death_Cause,name = 'add_death_cause'),
	path('Admin/death-cause-list/',views.Death_Cause_List,name = 'death_cause_list'),

	path('Admin/movement_certificate/<id>/',views.Movement_Cert,name = 'movement_certificate'),
	path('Admin/movement_certificate_print/<id>/',views.Print_Movement_Cert,name = 'movement_certificate_print'),



	path('Admin/wait/',views.Wait,name = 'wait'),



]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
