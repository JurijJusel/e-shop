from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Hat(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(1000)]
        )
    image = models.ImageField(upload_to='hat_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.price} EUR"
