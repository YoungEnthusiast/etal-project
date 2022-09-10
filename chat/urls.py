from django.urls import path
from chat import views

urlpatterns = [
    # path('lobby', views.lobby, name='lobby'),
    path('<str:id>/chat/', views.index, name='chat'),
    # path('chat/<str:room_name>/<str:someone>/', views.room, name='room'),
    path('<str:id>/chat/<str:room_name>/', views.room, name='room'),


]
