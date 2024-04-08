from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from datetime import datetime

from StockWebsite.utils import API_call, quicksort, linear_search, create_graph
from accounts.models import CustomUser
from portfolio.models import Order
from .models import Stock
from django.contrib.auth.decorators import login_required


# Function to find the partition position


# Create your views here.

def index(request, sort="", search=""):
    # Main page funktion der bliver kørt når siden loades

    results = API_call(
        "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-03-06?adjusted=true&apiKey=")
    # Udtag results fra data

    # Sorter liste på baggrund af trading volume ('v')
    sorted_results = quicksort(
        results, 0, len(results)-1, 'v', descending=True)

    # Udvælg de 100 mest handlede aktier
    top_100_companies = sorted_results[:100]

    if sort == 'ticker':
        stocks = quicksort(top_100_companies, 0,
                           len(top_100_companies)-1, 'T')
    elif sort == 'price':
        stocks = quicksort(top_100_companies, 0,
                           len(top_100_companies)-1, 'c', descending=True)
    elif search:
        search_result = linear_search(top_100_companies, search.upper())
        if search_result != -1:
            stocks = [search_result]
        else:
            stocks = []
    else:
        stocks = top_100_companies

    # Render templaten index.html
    return render(request, "stocks/index.html", {"stocks": stocks})


def detail(request, stock_ticker):

    # Api request
    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")

    graph_data = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                          "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    graph, price = create_graph(graph_data)

    news = API_call(
        "https://api.polygon.io/v2/reference/news?ticker=", stock_ticker, "&limit=3&apiKey=")

    return render(request, 'stocks/detail.html', {'stock': ticker_results, 'graph': graph, 'price': price, 'news': news})


@login_required
def process(request, stock_ticker, quantity, price):

    # opret en ordre her og redirect til portfolio

    cost = quantity * price

    # fra https://docs.djangoproject.com/en/dev/ref/models/querysets/#get-or-create
    stock_obj, created = Stock.objects.get_or_create(
        price=price,
        ticker=stock_ticker,
        transactionDate=datetime.now().replace(second=0, microsecond=0)

    )

    order_obj = Order(quantity=quantity, user=request.user, stock=stock_obj)

    currentUser = request.user

    currentUser.balance = currentUser.balance-cost

    order_obj.save()
    currentUser.save()

    return render(request, 'stocks/process_trade.html', {'stockTicker': stock_ticker, 'quantity': quantity, 'price': price})


def redirect(request):
    return render(request, 'portfolio/index.html')


@login_required
def handle_transaction(request, stock_ticker):

    price_results = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                             "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")
    # Udtag results fra data

    price = get_price(price_results)
    name, ticker = get_name_and_ticker(ticker_results)

    return render(request, 'stocks/handle_transaction.html', {'price': price, 'name': name, 'ticker': ticker})


@login_required
def sell(request, stock_ticker):
    price_results = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                             "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")
    # Udtag results fra data

    price = get_price(price_results)
    name, ticker = get_name_and_ticker(ticker_results)

    return render(request, 'stocks/sell.html', {'price': price, 'name': name, 'ticker': ticker})


def get_price(data):
    closeList = []
    for price in data:
        for category in price:
            if category == 'c':
                closeList.append(price[category])
    return closeList[-1]


def get_name_and_ticker(data):
    name = data['name']
    ticker = data['ticker']
    return name, ticker
