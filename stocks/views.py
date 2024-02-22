from django.http import HttpResponse
from django.shortcuts import render
from .models import Stock

# Create your views here.


def index(request):
    # Main page funktion der bliver kørt når siden loades
    # Henter alle stocks fra databasen. Svarer til SELECT * FROM stocks_stock
    stocks = Stock.objects.all()  # Kaldes abstraction api
    output = ", ".join([m.name for m in stocks])
    return HttpResponse(output)
