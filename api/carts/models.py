from django.db import models
from api.customers.models import Customer
from api.products.models import Product


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(product.price for product in self.products.all())

    def __str__(self):
        return f"Cart #{self.id} for {self.customer.email}"

    class Meta:
        ordering = ['-created_at']
