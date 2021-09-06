from django.urls import path
from . import views, ajax_view

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('ajax_payment/', views.ajax_payment, name='ajax_payment'),
    path('pay_with_paystack/', ajax_view.AjaxPayment.as_view(), name='pay_with_paystack'),
    path('<int:id>/pdf', views.Pdf.as_view(), name='render_pdf'),
]