from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from StockWebsite.utils import API_call, quicksort, linear_search
from .models import Stock
from django.contrib.auth.decorators import login_required

from plotly import graph_objects as go
import pandas as pd

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
def process(request, stock_ticker, quantity, type, price):

    # opret en ordre her og redirect til portfolio

    return render(request, 'stocks/process_trade.html', {'stockTicker': stock_ticker, 'quantity': quantity, 'price': price, 'type': type})


@login_required
def buy(request, stock_ticker):
    price_results = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                             "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")
    # Udtag results fra data

    price = get_price(price_results)
    name, ticker = get_name_and_ticker(ticker_results)

    return render(request, 'stocks/buy.html', {'price': price, 'name': name, 'ticker': ticker})


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


def create_graph(graph_data):
    # Udtag results fra data

    rawData = graph_data

    closeList = []
    openList = []
    highList = []
    lowList = []
    timeList = []

    for bar in rawData:
        for category in bar:
            if category == 'c':
                closeList.append(bar[category])
            elif category == "h":
                highList.append(bar[category])
            elif category == 'l':
                lowList.append(bar[category])
            elif category == 'o':
                openList.append(bar[category])
            elif category == 't':
                timeList.append(bar[category])

    price = closeList[-1]

    # Konverter tid i millisekunder til datoer
    times = []
    for time in timeList:
        times.append(pd.Timestamp(time, tz='GMT', unit='ms'))

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=times, open=openList,
                  high=highList, low=lowList, close=closeList, name='graph'))
    fig.update_layout(xaxis_rangeslider_visible=False)

    graph = fig.to_html()
    return graph, price


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
