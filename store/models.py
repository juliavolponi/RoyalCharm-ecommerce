from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    category = models.CharField(max_length=100, choices=[
        ('necklace', 'Necklace'),
        ('earring', 'Earring'),
        ('ring', 'Ring'),
        ('bracelet', 'Bracelet'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
