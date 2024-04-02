from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Stock
import requests
from plotly import graph_objects as go
import pandas as pd

# Function to find the partition position


def partition(array, low, high, sort_by, descending):

    # Choose the rightmost element as pivot
    pivot = array[high][sort_by]
    # Pointer for greater element
    i = low - 1
    # Traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if descending:
            if array[j][sort_by] >= pivot:
                # If element greater than pivot is found
                # swap it with the smaller element pointed by i
                i = i + 1
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
        else:
            if array[j][sort_by] <= pivot:
                # If element smaller than pivot is found
                # swap it with the greater element pointed by i
                i = i + 1
                # Swapping element at i with element at j
                (array[i], array[j]) = (array[j], array[i])
    # Swap the pivot element with
    # the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])
    # Return the position from where partition is done
    return i + 1


def quicksort(array, low, high, sort_by, descending=False):
    if low < high:
        # Find pivot element such that
        # element smaller than pivot are on the left
        # element greater than pivot are on the right
        pi = partition(array, low, high, sort_by, descending)
        # Recursive call on the left of pivot
        quicksort(array, low, pi - 1, sort_by, descending)
        # Recursive call on the right of pivot
        quicksort(array, pi + 1, high, sort_by, descending)
        
    return array


# Create your views here.

def index(request, sort=None):
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
    else:
        stocks = top_100_companies

    # Render templaten index.html
    return render(request, "stocks/index.html", {"stocks": stocks})


def detail(request, stock_ticker):

    # Api request
    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")
    # Udtag results fra data

    graph_data = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                          "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    graph, price = create_graph(graph_data)

    news = API_call(
        "https://api.polygon.io/v2/reference/news?ticker=", stock_ticker, "&limit=3&apiKey=")
    # Udtag results fra data

    return render(request, 'stocks/detail.html', {'stock': ticker_results, 'graph': graph, 'price': price, 'news': news})


def buy(request, stock_ticker):
    price_results = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                             "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")
    # Udtag results fra data

    price = get_price(price_results)
    name, ticker = get_name_and_ticker(ticker_results)

    return render(request, 'stocks/buy.html', {'price': price, 'name': name, 'ticker': ticker})


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


def API_call(url1, stockTicker="", url2=""):
    api_key_1 = "d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"
    api_key_2 = "0q2Jm5XhAiiz72Bq2lwRBx3zxIiaOJnj"
    api_key_3 = "qKBhJuyKplmty3xvzKW0mJmOhn25O_dY"
    apiKey = api_key_1
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
    return (data['results'])


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
