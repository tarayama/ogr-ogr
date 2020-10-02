from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  #login前ページ
    path('top/<str:user>', views.top, name='top'),  #login後topページ
    path('mypage/<str:user>', views.my_page, name='my_page'),
    path('addfriend', views.addfriend, name='addfriend'),
    path('create', views.create_log, name='create_log'),  #log作成画面
    path('detail/<int:ogr_id>', views.detail, name='detail'),
    path('delete/<int:ogr_id>', views.delete, name='delete'),
]
