from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Stock

# Create your views here.


def index(request):
    # Main page funktion der bliver kørt når siden loades
    # Henter alle stocks fra databasen. Svarer til SELECT * FROM stocks_stock
    stocks = Stock.objects.all()  # Kaldes abstraction api
    # Render templaten index.html
    return render(request, "stocks/index.html", {"stocks": stocks})


def detail(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    return render(request, 'stocks/detail.html', {'stock': stock})
