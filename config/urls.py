"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from ogr.error import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ogr.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('linebot/',include('Linebot.urls')),
    path('api/', include('api.urls')),
]


handler400 = my_customized_server400_error
handler403 = my_customized_server403_error
handler404 = my_customized_server404_error
handler500 = my_customized_server500_error
