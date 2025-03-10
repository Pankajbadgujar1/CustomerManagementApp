from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return HttpResponse("Hello, Account App page Django!")

def contact(request):
    return HttpResponse(" Account app Contact Page")