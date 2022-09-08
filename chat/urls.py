from django.urls import path
from chat import views

urlpatterns = [
    path('lobby', views.lobby, name='lobby'),

]
