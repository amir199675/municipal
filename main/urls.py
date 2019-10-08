from django.urls import path
from . import api_views
from .views import *


app_name = 'Main'
urlpatterns = [

	path('', Index, name='index'),
	path('memorials/', Memorial, name='memorials'),
	path('about-us/', About_Us, name='about_us'),
	path('search/', Search, name='search'),
	path('all-news/', All_News, name='all_news'),
	path('contact', Contact, name='contact'),


	path('api/v1/chanters/', api_views.APIListMadah.as_view()),
	path('api/v1/advance_search_dead/',api_views.DeceasedAdvanceSearchAPIView.as_view()),
	path('api/v1/after_death/CreateList/',api_views.After_DeathCreateAPIView.as_view()),
	path('api/v1/simple_search_dead/',api_views.DeceasedSimpleSearchAPIView.as_view()),
	path('api/v1/after_death_get/',api_views.After_Death_GetAPIView.as_view()),

]
