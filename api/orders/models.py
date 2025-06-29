from django.db import models
from api.customers.models import Customer
from api.carts.models import Cart
from django.core.validators import MinValueValidator
from decimal import Decimal


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_total(self):
        if self.cart:
            total = self.cart.total_price()
            self.amount_paid = total
            self.save()
            return total
        return Decimal('0.00')

    def __str__(self):
        return f"Order #{self.id} by {self.customer.email}"

    class Meta:
        ordering = ['-created_at']


class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='statuses')
    delivery_status = models.CharField(max_length=20, blank=True, null=True)
    order_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('processing', 'Processing'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
            ('canceled', 'Canceled')
        ],
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('unpaid', 'Unpaid'),
            ('paid', 'Paid'),
            ('refunded', 'Refunded')
        ],
        default='unpaid'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order.id} - Status: {self.order_status} - Payment: {self.payment_status}"

    class Meta:
        ordering = ['-created_at']
