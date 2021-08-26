from django.urls import path
from . import views
app_name = 'users'

urlpatterns = [
    path('sign_up/', views.signup_view, name='sign_up'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]