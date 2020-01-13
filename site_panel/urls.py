from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views , payment , movement_views



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

	path('Admin/add-service/',payment.Add_Service,name = 'add_service'),
	path('Admin/service-list/',payment.Services,name = 'service-list'),
	path('Admin/service-list/edit/<id>/',payment.Edit_Service,name = 'edit_service'),

	path('Admin/add-letter/',views.Add_Letter,name = 'add_letter'),
	path('Admin/inbox-letter/',views.Inbox_Letter,name = 'inbox_letter'),
	path('Admin/send-list/',views.Send_List,name = 'send_list'),
	path('Admin/inbox-list/',views.Receive_List,name = 'inbox_list'),
	path('Admin/edit-send-letter/<code_slug>/',views.Edit_Send_Letter,name = 'edit_send_letter'),
	path('Admin/edit-receive-letter/<code_slug>/',views.Edit_Receive_Letter,name = 'edit_receive_letter'),

	path('Admin/add-death-cause/',views.Add_Death_Cause,name = 'add_death_cause'),
	path('Admin/death-cause-list/',views.Death_Cause_List,name = 'death_cause_list'),


	path('Admin/add_target/',movement_views.Add_Target,name = 'add_target'),
	path('Admin/edit_target/<id>/',movement_views.Edit_Target,name = 'edit_target'),
	path('Admin/target_list/',movement_views.Target_List,name = 'target_list'),
	path('Admin/movement_license/<id>/',movement_views.Movement_Lic,name = 'movement_license'),
	path('Admin/movement_license_list/<id>/',movement_views.Movement_License_List,name = 'movement_license_list'),

	# path('Admin/movement_certificate_print/<id>/',views.Print_Movement_Cert,name = 'movement_certificate_print'),

	path('Admin/all_user/',payment.User_list,name = 'user_list'),
	path('Admin/edit_user/<id>/',payment.Edit_User,name = 'edit_user'),
	path('Admin/reserve_factor/',payment.Reserve_Factor,name = 'reserve_factor'),
	path('Admin/factor_list/',payment.Factor_List,name = 'factor_list'),
	path('Admin/factor_details/<document>/',payment.Factor_Details,name = 'factor_details'),
	path('Admin/factor_print/<document>/',payment.Print_Factor,name = 'print_factor'),

	path('Admin/place_pre_sell/',payment.Place_Pre_Sell,name = 'place_pre_sell'),
	path('Admin/add_user/',payment.Add_User,name = 'add_user'),

	path('Admin/driver_list/',movement_views.Driver_List,name = 'driver_list'),
	path('Admin/add_driver/',movement_views.Add_Driver,name = 'add_driver'),
	path('Admin/edit_driver/<id>/',movement_views.Edit_Driver,name = 'edit_driver'),
	path('Admin/movement_list/',movement_views.Census_Movement,name = 'movement_list'),

	path('Admin/census_deceased/',views.Census_Deceased,name = 'census_deceased'),





	path('Admin/wait/',views.Wait,name = 'wait'),



]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
