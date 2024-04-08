import dataclasses
from django.shortcuts import render
from django.http import HttpResponse

from stocks.models import Stock
from .models import Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
import requests
from plotly import graph_objects as go
import pandas as pd
from .models import Order
from StockWebsite.utils import quicksort, linear_search, get_price, get_name_and_ticker, API_call
from django.http import JsonResponse
# Create your views here.

@login_required
def index(request, sort=None):

    # Fetch orders fra database
    orders = Order.objects.filter(user=request.user, isActive=True)
    
    if sort == 'price':
            #sorter orders med price via quicksort
            orders= sorted(orders, key=lambda x: x.stock.price, reverse=True)

    for order in orders:
        price_results = API_call("https://api.polygon.io/v2/aggs/ticker/", order.stock.ticker,
                             "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")
        price = get_price(price_results)
        if price is not None:
             order.current_price = price
    
    

        #order.current_price = get_price(ticker_results)
    



    return render(request, "index.html", {"orders": orders})

def sell_stock(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.isActive = False
    order.save()
    return JsonResponse({'message': 'Stock sold successfully'}, status=200)

    #Hent pris fra aktier gennem API
    
    #Ny forsøg:

    # Fetch orders from database
    #orders = Order.objects.filter(user=request.user, isActive=True)

    #if sort == 'price':
        # Sort orders by price using quicksort
     #   orders = orders.order_by('-price')  # Assuming you want descending order by price

    #return render(request, "index.html", {"orders": orders})

