from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=255)
    external_url = models.URLField(unique=True)

    def __str__(self):
        return self.name

class ShortenedURL(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    short_url = models.CharField(max_length=10, unique=True)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.short_url
