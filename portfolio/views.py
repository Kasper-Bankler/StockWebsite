import dataclasses
from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Stock
import requests
from plotly import graph_objects as go
import pandas as pd
# Create your views here.


#@login_required
def index(request, sort=None):
    # Render templaten index.html
    # return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    data = Order.objects.all  # Henter alt data fra orders i databasen

    data = API_call(
        "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-03-06?adjusted=true&apiKey=", api_key_1)
    # Udtag results fra data
    results = data['results']

    # Sorter liste på baggrund af trading volume ('v')
    sorted_results = sorted(results, key=lambda x: x['v'], reverse=True)

    # Udvælg de 100 mest handlede aktier
    top_100_companies = sorted_results[:100]

    if sort == 'ticker':
        stocks = sorted(top_100_companies, key=lambda x: x['T'], reverse=False)
    elif sort == 'price':
        stocks = sorted(top_100_companies, key=lambda x: x['c'], reverse=True)
    else:
        stocks = top_100_companies

    # Render templaten index.html
    
    return render(request, "index2.html", {"orders": Order})


def API_call(url1, apiKey="", stockTicker="", url2=""):
    headers = {
        "Authorization": "Bearer "+apiKey
    }
    if (stockTicker != ""):
        callUrl = url1+stockTicker+url2+apiKey
        response = requests.get(callUrl, headers=headers)
    else:
        callUrl = url1+apiKey
        response = requests.get(callUrl, headers=headers)
    data = response.json()
    return (data)

api_key_1 = "d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"
