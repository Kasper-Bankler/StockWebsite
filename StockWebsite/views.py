from django.shortcuts import render
#from .models import Portfolio
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def index(request):
    portfolio = Portfolio.objects.all()
    return render(request, "index2.html", {"portfolio": portfolio})


