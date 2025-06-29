from django.db import models

class Customer(models.Model):
    customer_id = models.CharField(max_length=32, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=64)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_id or 'Guest'} - {self.email} - {self.phone}"

