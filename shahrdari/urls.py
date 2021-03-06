"""shahrdari URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from  site_panel.tasks import scheduler , delete_last_seen

app_name = 'Master'
urlpatterns = [
    path('SuperAdmin/', admin.site.urls),
    path('',include('main.urls',namespace='Main')),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('',include('site_panel.urls',namespace='Site_Panel')),
    path('Account/',include('Account.urls',namespace='Account')),
    path('Seen/',include('seen.urls',namespace='Seen')),
]


scheduler.start()

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
