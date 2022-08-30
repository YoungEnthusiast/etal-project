from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
from .views import ActivateAccount

urlpatterns = [
    path('join', views.create, name='account'),
    path('where-next/', views.loginTo),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='activate'),
    path('dashboard', views.showResearcherBoard, name='researcher_board'),
    path('profile', views.showResearcherProfile, name='researcher_profile'),
    path('collab', views.showCollabs, name='collab'),
    path('collab/create-collab', views.createCollab, name='create_collab'),
    path('', views.showHome, name='index'),
    path('collab/view-researcher/<str:email>/', views.showUser, name='show_user'),
    path('collab/view/<str:id>/', views.showCollab, name='show_collab'),
    path('collab/view/<str:id>/update', views.updateCollab, name='update_collab'),
    path('collab/view/<str:id>/delete', views.deleteCollab, name='delete_collab'),

    path('collab/view-initiated/<str:id>/', views.showCollabInitiated, name='show_collab_initiated'),
    path('collab/view-initiated/<str:id>/removed/<str:username>', views.removeCollab, name='remove_collab'),
    path('collab/view-accepted/<str:id>/', views.showCollabAccepted, name='show_collab_accepted'),
    path('collab/view-accepted/<str:id>/left/<str:username>', views.leaveCollab, name='leave_collab'),
    path('collab/view/<str:id>/offered/<str:username>', views.offerCollab, name='offer_collab'),
    path('collab/view/<str:id>/declined/<str:username>', views.declineCollab, name='decline_collab'),

    path('collabs', views.collabs, name='collabs'),
    path('initiated-collabs', views.initiatedCollabs, name='initiated_collabs'),
    path('accepted-collabs', views.acceptedCollabs, name='accepted_collabs'),
    path('bell-notification', views.clearUnreads, name='bell_notification'),
    path('bell-notifications', views.showBellNotifications, name='bell_notifications'),
    path('collab/interested/<int:id>', views.interestCollab, name='interest_collab'),
    path('collab/locked/<int:id>', views.lockCollab, name='lock_collab'),
    path('collab/unlocked/<int:id>', views.unlockCollab, name='unlock_collab'),
    path('collab/undo-interest/<int:id>', views.undoInterestCollab, name='undo_interest_collab'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/login.html'), name='logout'),


]
