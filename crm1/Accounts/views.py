from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'Accounts/dashboard.html')
    #return HttpResponse("Hello, Account App page Django!")

def customer(request):
    return render(request, 'Accounts/customer.html')
    #return HttpResponse(" Account app Contact Page")


def products(request):
    return render(request, 'Accounts/products.html')