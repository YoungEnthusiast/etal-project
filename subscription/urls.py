from django.urls import path
from subscription import views

urlpatterns = [
    path('billings-and-plans', views.plans, name='plans'),
    path('upgrade', views.upgrade, name='upgrade_page'),
    path('history', views.history, name='history'),
]
