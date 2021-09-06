from django.http import JsonResponse
from django.views import View
from .models import Order


class AjaxPayment(View):

    def get(self, request):
        id = request.GET.get('id', None)
        reference_id = request.GET.get('reference', None)
        order_detail = Order.objects.get(id=id)
        data = {}

        order_detail.reference_id = reference_id
        order_detail.paid = True
        order_detail.save()

        if order_detail.paid:
            data['message'] = "Your Payment was successfully received"
        else:
            data['message'] = "Your Payment Failed!!!"
        return JsonResponse(data)
