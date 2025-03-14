from django.forms import inlineformset_factory
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm ,CreateUserForm,CustomerForm
from .filters import OrderFilter
from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate,login , logout
#django built-in decorator
from django.contrib.auth.decorators import login_required
#djnago custome decoratior
from .decorators import unauthenticated_user, allowed_users
#creating login and register 
def registerPage(request):
    form = CreateUserForm()
    if request.method =="POST":
        form =CreateUserForm(request.POST)
        if form.is_valid():
            user =form.save()
            print("user created successfully: ", user.username)
            print("user created successfully")
            username = form.cleaned_data.get("username")
            try:

                group = Group.objects.get(name= 'Customer')
                print('group found',group.name)
                user.groups.add(group)
                print("user added to group")
            except Group.DoesNotExist:
                print("Group 'Customer does not exit")
                
            Customer.objects.create(user=user)


            messages.success(request, 'Accuout was created for ' + user.username)
            return redirect('login')

    context = {'form':form}
    return render(request,'Accounts/register.html',context)


#-------------------------------------------------------------------------------------------------------
@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def accountSetting(request):
    customer =request.user.customer
    form = CustomerForm(instance=customer)

    if request.method  =='POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request,'Accounts/account.html',context)

#-------------------------------------------------------------------------------------------------------

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request,username=username ,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"Username or password is incorrect")
            return render(request,'Accounts/login.html')

  
    context = {}
    return render(request,'Accounts/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

# Create your views here.
#This is create order view
@login_required(login_url='login')

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
@login_required(login_url='login')
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['Customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status ='Delivered').count()
    pending = orders.filter(status ='Pending').count()
   
    context ={'orders':orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers,'delivered':delivered,'pending':pending }
    return render(request,'Accounts/user.html' ,context )


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','staff'])
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

@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()

    MyFilter = OrderFilter(request.GET, queryset=orders)
    orders = MyFilter.qs

    context = {'customer':customer, 'orders':orders, 'MyFilter':MyFilter}
    return render(request, 'Accounts/customer.html',context)
    #return HttpResponse(" Account app Contact Page")

@login_required(login_url='login')
def products(request):
    product = Product.objects.all()
    return render(request, 'Accounts/products.html', {'product':product})