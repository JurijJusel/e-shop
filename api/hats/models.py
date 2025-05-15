from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Hat(models.Model):
    name = models.CharField(max_length=100, blank=False, null=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
        )
    image = models.ImageField(upload_to='hat_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} EUR"


class HatImage(models.Model):
    hat = models.ForeignKey(Hat, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hat_images/')
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.hat.name}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.email} - {self.phone}"
        return f"Guest - {self.email} - {self.phone}"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def total_price(self):
        return sum(item.unit_price for item in self.items.all())

    def __str__(self):
        return f"Cart #{self.id} for {self.customer.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,  related_name='items', on_delete=models.CASCADE)
    hat = models.ForeignKey(Hat, on_delete=models.CASCADE)
    unit_price = models.IntegerField()

    class Meta:
        unique_together = ('cart', 'hat')

    def __str__(self):
        return f"{self.hat.name} in cart #{self.cart.id}"


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    total_amount = models.IntegerField()
    payment_method = models.CharField(max_length=20, blank=True)
    payment_status = models.CharField(max_length=10, default='unpaid')

    def calculate_total(self):
        total = sum(item.unit_price for item in self.items.all())
        self.total_amount = total
        return total

    def __str__(self):
        return f"Order #{self.id} by {self.customer.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    hat = models.ForeignKey(Hat, on_delete=models.PROTECT)
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.hat.name} @ {self.unit_price}€ in order #{self.order.id}"
