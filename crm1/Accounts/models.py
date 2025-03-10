from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone= models.CharField(max_length=10)
    email =models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)
    