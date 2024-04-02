from django.shortcuts import render
#from .models import Portfolio
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def index(request):
    portfolio = portfolio.objects.all()
    return render(request, "index.html", {"portfolio": portfolio})


