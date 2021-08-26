from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
    path('admin_signup/', views.AdminSignUpView.as_view(), name='admin_signup'),
    path('admin_login/', views.admin_user_login, name='admin_login'),
    path('admin_update/', views.update_profile, name='admin_update'),
    path('logout/', views.user_logout, name='logout'),
]