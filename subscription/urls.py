from django.urls import path
from subscription import views

urlpatterns = [
    path('billings-and-plans', views.plans, name='plans'),
    path('upgrade', views.upgrade, name='upgrade'),
    path('history', views.history, name='history'),
    path('history/receipt/<str:id>', views.receipt, name='receipt'),
    path('pay-monthly', views.monthly, name='monthly'),
    path('pay-yearly', views.yearly, name='yearly'),
]
