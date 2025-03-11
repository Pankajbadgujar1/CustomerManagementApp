from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone= models.CharField(max_length=10)
    email =models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    CATEGORY = {
        ('Indore', 'Indore'),
        ('Out Door','Out Door'),
    }
    name = models.CharField(max_length=200)
    price =models.FloatField(null=True)
    category = models.CharField(max_length=200, choices=CATEGORY)
    description = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name
    


    
class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True ,on_delete=models.SET_NULL)
    product = models.ForeignKey(Product,null=True, on_delete= models.SET_NULL)
    STATUS = {
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Delivered','Delivered')
    }

    date_created =models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    
    def __str__(self):
        return self.product.name