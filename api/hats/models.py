from django.db import models

class Hat(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='hat_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
