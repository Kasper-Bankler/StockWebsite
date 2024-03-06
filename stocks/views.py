from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Stock
import requests


# Create your views here.


def index(request):
    # Main page funktion der bliver kørt når siden loades
    # Henter alle stocks fra databasen. Svarer til SELECT * FROM stocks_stock
    stocks = Stock.objects.all()  # Kaldes abstraction api

    url = "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2023-01-09?adjusted=true&apiKey=d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"

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


def detail(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    return render(request, 'stocks/detail.html', {'stock': stock})
