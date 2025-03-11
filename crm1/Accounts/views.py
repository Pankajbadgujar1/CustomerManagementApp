from django.forms import inlineformset_factory
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from .filters import OrderFilter
# Create your views here.
#This is create order view
def create_Order(request, pkk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields= ('product','status'), extra=10)
    customer = Customer.objects.get(id=pkk)
    formset = OrderFormSet( queryset= Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method =="POST":
        #print('printiong post',request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset':formset}
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

    MyFilter = OrderFilter(request.GET, queryset=orders)
    orders = MyFilter.qs

    context = {'customer':customer, 'orders':orders, 'MyFilter':MyFilter}
    return render(request, 'Accounts/customer.html',context)
    #return HttpResponse(" Account app Contact Page")


def products(request):
    product = Product.objects.all()
    return render(request, 'Accounts/products.html', {'product':product})