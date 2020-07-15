from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('b/', views.b, name='inde'),
    path('<str:room_name>/', views.room, name='room'),
]