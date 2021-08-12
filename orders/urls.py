from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('ajax_payment/', views.ajax_payment, name='ajax_payment'),
    path('<int:id>/pdf', views.Pdf.as_view(), name='render_pdf'),
]