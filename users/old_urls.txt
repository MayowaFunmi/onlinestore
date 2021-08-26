from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
    path('admin_signup/', views.AdminSignUpView.as_view(), name='admin_signup'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name='activate'),
    path('register/', views.AdminRegister.as_view(), name='register'),
    path('signup_success/', views.SignUpSuccess, name='signup_success'),
    path('get_admin_code/', views.get_code, name='get_admin_code'),
    path('admin_login/', views.admin_user_login, name='admin_login')

]