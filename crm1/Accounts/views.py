from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
# Create your views here.
#This is create order view
def create_Order(request):
    form = OrderForm()
    if request.method =="POST":
        #print('printiong post',request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request,'Accounts/order_form.html' ,context )

#update order view
def update_Order(request,pkk):
    order = Order.objects.get(id =pkk)
    form = OrderForm(instance=order) 
    if request.method =="POST":
        #print('printiong post',request.POST)
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request,'Accounts/order_form.html' ,context )

def delete_Order(request, pkk):
    order = Order.objects.get(id=pkk)

    if request.method =="POST":
        order.delete()
        return redirect('home')

    context= {'item':order}
    return render(request,'Accounts/delete.html' ,context )


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