from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('9999.99'))
        ]
    )
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} EUR"

    class Meta:
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image for {self.product.name}"

    class Meta:
        ordering = ['-created_at']


class Customer(models.Model):
    customer_id = models.CharField(max_length=32, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=64)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_id or 'Guest'} - {self.email} - {self.phone}"

    class Meta:
        ordering = ['-created_at']


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
