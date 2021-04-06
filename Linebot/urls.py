from django.urls import path
from . import views

urlpatterns = [
    path('callback', views.callback, name='callback'), 
    path('link/<str:Line_user_id>/<str:linkToken>', views.get_django_userid_and_redirect_line, name="linelink")
]
