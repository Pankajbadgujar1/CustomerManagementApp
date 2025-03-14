from django.contrib import admin

# Register your models here.
from .models import Customer,Product,Order,Tag,Profile

admin.site.register(Customer)

admin.site.register(Product)

admin.site.register(Order)

admin.site.register(Tag)

admin.site.register(Profile)