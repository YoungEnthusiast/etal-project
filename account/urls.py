from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
from .views import ActivateAccount

urlpatterns = [
    path('join', views.create, name='account'),
    # path('where-next/', views.loginTo),
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('activate/<uidb64>/<token>', ActivateAccount.as_view(), name='activate'),

    # path('logout/', auth_views.LogoutView.as_view(template_name='account/login.html'), name='logout'),


    # path('researcher-dashboard/edit-profile', views.editQwikCust, name='qwikcust_profile'),
    # path('collaborator-dashboard/edit-profile', views.editcollaborator, name='collaborator_profile'),
    # path('admin-dashboard/edit-profile', views.editadmin, name='admin_profile'),
    # path('superadmin-dashboard/edit-profile', views.editsuperadmindmin, name='superadmindmin_profile'),
    # path('superadmin-dashboard/all-account', views.showsuperadmindminPeople, name='superadmindmin_people'),
    # path('superadmin-dashboard/all-account/export-csv', views.exportCSVPeople, name='export_csv_people'),
    # path('researcher-dashboard/edit-profile/change-password', views.changePasswordQwikCust, name='qwikcust_change_password'),
    # path('collaborator-dashboard/edit-profile/change-password', views.changePasswordcollaborator, name='collaborator_change_password'),
    # path('admin-dashboard/edit-profile/change-password', views.changePasswordadmin, name='admin_change_password'),
    # path('superadmin-dashboard/edit-profile/change-password', views.changePasswordsuperadmindmin, name='superadmindmin_change_password'),
    # path('reset-password', auth_views.PasswordResetView.as_view(template_name='account/reset_password.html'), name='reset_password'),
    # path('reset-password-sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_sent.html'), name='password_reset_done'),
    # path('reset-password/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_form.html'), name='password_reset_confirm'),
    # path('reset-password-complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_done.html'), name='password_reset_complete'),
    # path('researcher-dashboard', views.showQwikCustBoard, name='qwikcust_board'),
    # path('researcher_dashboard', views.showFirstLogin, name='first_login'),
    # path('collaborator-dashboard', views.showcollaboratorBoard, name='collaborator_board'),
    # path('admin-dashboard', views.showadminBoard, name='admin_board'),
    # path('superadmin-dashboard', views.showsuperadmindminBoard, name='superadmindmin_board'),
    # path('superadmin-dashboard/user/update/<int:id>', views.updatePerson, name='person_update'),
    # path('superadmin-dashboard/user/delete/<int:id>', views.deletePerson),
    # path('superadmin-dashboard/outlets', views.showsuperadmindminOutlets, name='superadmindmin_outlets'),
    # path('superadmin-dashboard/outlets/export-csv', views.exportCSVOutlets, name='export_csv_outlets'),
    # path('superadmin-dashboard/outlet/update/<int:id>', views.updateOutlet, name='outlet_update'),
    # path('superadmin-dashboard/outlet/add-new', views.addOutlet, name='superadmindmin_outlet'),
    # path('superadmin-dashboard/outlet/delete/<int:id>', views.deleteOutlet),
    # path('researcher-dashboard/wallet-histories', views.showQwikCustWallets, name='qwikcust_wallets'),
    # # path('researcher-dashboard/wallet-histories/request-credit', views.requestCredit, name='bb'),
    #
    # path('superadmin-dashboard/wallet-histories', views.showsuperadmindminWallets, name='superadmindmin_wallets'),
    # path('superadmin-dashboard/credit-wallet', views.creditWallet, name='wallet_credit'),
    # path('reg-gas-ister', views.createUser, name='superadmindmin_account'),
]
