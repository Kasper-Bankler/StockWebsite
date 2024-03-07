from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Stock
import requests


# Create your views here.

def index(request):
    # Main page funktion der bliver kørt når siden loades
    # Henter alle stocks fra databasen. Svarer til SELECT * FROM stocks_stock
    stocks = Stock.objects.all()  # Kaldes abstraction api

    url = "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-03-06?adjusted=true&apiKey=d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"

    headers = {
        "Authorization": "Bearer d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Udtag results fra data
    results = data['results']

    # Sorter liste på baggrund af trading volume ('v')
    sorted_results = sorted(results, key=lambda x: x['v'], reverse=True)

    # Udvælg de 100 mest handlede aktier
    top_100_companies = sorted_results[:100]

    # Render templaten index.html
    return render(request, "stocks/index.html", {"stocks": top_100_companies})


def detail(request, stock_ticker):
    url = "https://api.polygon.io/v3/reference/tickers?ticker=" + \
        stock_ticker+"&active=true&apiKey=0q2Jm5XhAiiz72Bq2lwRBx3zxIiaOJnj"

    headers = {
        "Authorization": "Bearer 0q2Jm5XhAiiz72Bq2lwRBx3zxIiaOJnj"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    # Udtag results fra data
    results = data['results']
    print(results)

    return render(request, 'stocks/detail.html', {'stock': results})
