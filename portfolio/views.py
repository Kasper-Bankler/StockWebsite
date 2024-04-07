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
from StockWebsite.utils import quicksort, linear_search
# Create your views here.

@login_required
def index(request, sort=None):

    stocks=Stock.objects.all()
    for stock in stocks:
        print(stock.transactionDate)
    # Fetch orders fra database
    orders = Order.objects.filter(user=request.user, isActive=True)
    orders = list(orders.values())  # Konverterer orders til list af dictionaries

    if sort == 'price':
        # sorter orders med price via quicksort
        quicksort(orders, 0, len(orders) - 1, "price", descending=True)

    return render(request, "index.html", {"orders": orders})
