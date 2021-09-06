from django.db import models
from shop.models import Product
import random
import string
# Create your models here.


def random_code(digit=7, letter=3):
    sample_str = ''.join((random.choice(string.digits) for i in range(digit)))
    sample_str += ''.join((random.choice(string.ascii_uppercase) for i in range(letter)))

    sample_list = list(sample_str)
    final_string = ''.join(sample_list)
    return final_string


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    reference_id = models.CharField(max_length=200, null=True, blank=True)
    order_id = models.CharField(default=random_code, max_length=10, null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity