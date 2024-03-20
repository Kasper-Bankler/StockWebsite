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

    
    results = data['results']

    sorted_results = sorted(results, key=lambda x: x['v'], reverse=True)

    top_100_companies = sorted_results[:100]


    if sort == 'ticker':
        stocks = sorted(top_100_companies, key=lambda x: x['T'], reverse=False)
    elif sort == 'price':
        stocks = sorted(top_100_companies, key=lambda x: x['c'], reverse=True)
    else:
        stocks = top_100_companies

    try:
        if request.method == "POST":
            quantity = int(request.POST.get('quantity'))

    except:
        pass
    return render(request, "index2.html", {"orders": orders})


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
