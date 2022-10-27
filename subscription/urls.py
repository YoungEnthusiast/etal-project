from django.urls import path
from subscription import views

urlpatterns = [
    path('billings-and-plans', views.plans, name='plans'),
]
