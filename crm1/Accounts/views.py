from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count()
    context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers,'delivered':delivered,'pending':pending}
    return render(request, 'Accounts/dashboard.html' ,context)
    #return HttpResponse("Hello, Account App page Django!")

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    context = {'customer':customer, 'orders':orders}
    return render(request, 'Accounts/customer.html',context)
    #return HttpResponse(" Account app Contact Page")


def products(request):
    product = Product.objects.all()
    return render(request, 'Accounts/products.html', {'product':product})