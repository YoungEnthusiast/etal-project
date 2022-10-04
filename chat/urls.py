from django.urls import path
from chat import views

urlpatterns = [
    path('<str:id>/chat/', views.index, name='chat'),
    path('chat/<str:room_name>/', views.Room.as_view(), name='room'),
    path('envelope-notification', views.clearEnvelopeUnreads, name='envelope_notification'),
    path('envelope-notifications', views.showChatNotifications, name='envelope_notifications'),

]
