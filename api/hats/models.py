from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField


class Hat(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    image = models.ImageField(upload_to='hat_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} EUR"


class Customer(models.Model):
    customer_id = models.CharField(max_length=32, unique=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=64)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        if self.customer_id:
            return f"{self.customer_id} - {self.email} - {self.phone}"
        return f"Guest - {self.email} - {self.phone}"


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hats = models.ManyToManyField('Hat')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(hat.price for hat in self.hats.all())

    def __str__(self):
        return f"Cart #{self.id} for {self.customer.email}"


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
        return f"Order #{self.id} by {self.customer.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    hat = models.ForeignKey(Hat, on_delete=models.PROTECT)
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.hat.name} @ {self.unit_price}€ in order #{self.order.id}"
