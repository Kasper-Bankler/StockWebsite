from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Stock
import requests
from plotly import graph_objects as go
import pandas as pd


# Create your views here.

def APICall(url, stockTicker="", between=""):
    APICall.counter += 1
    apiKey1 = "d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"
    apiKey2 = "0q2Jm5XhAiiz72Bq2lwRBx3zxIiaOJnj"
    if (APICall.counter % 2 == 0):
        apiKey = apiKey1
    else:
        apiKey = apiKey2
    headers = {
        "Authorization": "Bearer "+apiKey
    }
    if (stockTicker != ""):
        callUrl = url+stockTicker+between+apiKey
        response = requests.get(callUrl, headers=headers)
    else:
        callUrl = url+apiKey
        response = requests.get(callUrl, headers=headers)
    data = response.json()
    return (data)


APICall.counter = 0


def index(request, sort=None):
    # Main page funktion der bliver kørt når siden loades

    data = APICall(
        "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-03-06?adjusted=true&apiKey=")
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
    return render(request, "stocks/index.html", {"stocks": stocks})


def detail(request, stock_ticker):

    # Api request
    ticker_data = APICall(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")
    # Udtag results fra data
    ticker_results = ticker_data['results']

    graph_data = APICall("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                         "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    graph, price = create_graph(graph_data)

    news_data = APICall(
        "https://api.polygon.io/v2/reference/news?ticker=", stock_ticker, "&limit=3&apiKey=")
    # Udtag results fra data
    news = news_data['results']

    return render(request, 'stocks/detail.html', {'stock': ticker_results, 'graph': graph, 'price': price, 'news': news})


def buy(request):

    return render(request, 'stocks/buy/.html')


def sell(request):

    return render(request, 'stocks/sell/.html')


def create_graph(graph_data):
    # Udtag results fra data

    for item in graph_data:
        if item == 'results':
            rawData = graph_data[item]

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
