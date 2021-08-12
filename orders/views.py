from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
# from .tasks import order_created

# views to render order report to pdf
from django.views.generic import View
from django.utils import timezone
from .render import Render

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # clear the cart
            # cart.clear()
            # launch asynchronous task
            # order_created.delay(order.id)
            context = {
                'order': order,
                'cart': cart,
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone_number']
            }
            return render(request, 'orders/pay_with_paystack.html', context)
    else:
        form = OrderCreateForm()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def ajax_payment(request):
    # order_req = get_object_or_404(Order, order_id)
    if request.is_ajax():
        reference_id = request.POST.get('reference')
        x = Order(reference=reference_id, paid=True)
        x.save()
        if x:
            response = {
                'message': "Your Payment was successfully received"
            }
            return JsonResponse(response)
        else:
            response = {
                'message': "Your Payment Failed"
            }
            return JsonResponse(response)


# view for pdf rendering
class Pdf(View):

    def get(self, request, id):
        cart = Cart(request)
        order_item = get_object_or_404(OrderItem, id=id)
        today = timezone.now()
        # clear the cart
        cart.clear()
        params = {
            'id': id,
            'today': today,
            'cart': cart,
            'order_item': order_item,
            # 'request': request
        }
        return Render.render('orders/order/pdf.html', params)