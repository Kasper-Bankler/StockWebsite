import dataclasses
from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
import requests
from plotly import graph_objects as go
import pandas as pd
from .models import Order
from StockWebsite.utils import quicksort
# Create your views here.


@login_required
def index(request, sort = None):
    # Render templaten index.html
    # return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    orders = Order.objects.filter(user=request.user,isActive=True).values()  # Henter alt data fra orders i databasen

    #fetch = Order.objects.all() #Dette henter alt data fra order databasen

    #return render(request, "index.html",
             #     {"fetch": fetch})

    # Render templaten index.html
    results = list(orders)
    
    sorted_results = quicksort(results, 0, len(results)-1, 'stock', descending=True)

    # Udvælg de 100 mest handlede aktier
    top_100_companies = sorted_results[:100]

    if sort == 'ticker':
        orders = quicksort(top_100_companies, 0,
                           len(top_100_companies)-1, 'T')
    elif sort == 'price':
        orders = quicksort(top_100_companies, 0,
                           len(top_100_companies)-1, 'c', descending=True)
    else:
        orders = top_100_companies
    
    return render(request, "index.html", {"orders": orders})
