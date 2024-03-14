from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from .models import Stock
import requests
from plotly import graph_objects as go
import pandas as pd


# Create your views here.

def index(request, sort=None):
    # Main page funktion der bliver kørt når siden loades

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

    if sort == 'ticker':
        stocks = sorted(top_100_companies, key=lambda x: x['T'], reverse=False)
    elif sort == 'price':
        stocks = sorted(top_100_companies, key=lambda x: x['c'], reverse=True)
    else:
        stocks = top_100_companies

    # Render templaten index.html
    return render(request, "stocks/index.html", {"stocks": stocks})


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

    url = "https://api.polygon.io/v2/aggs/ticker/"+stock_ticker + \
        "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"

    headers = {
        "Authorization": "Bearer d6fuLXExi6Y9gVzPW7OXwFhGxoKVk2qj"
    }

    response2 = requests.get(url, headers=headers)
    data2 = response2.json()
    # Udtag results fra data
    for item in data2:
        if item == 'results':
            rawData = data2[item]

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

    url = "https://api.polygon.io/v2/reference/news?ticker=" + \
        stock_ticker+"&limit=3&apiKey=0q2Jm5XhAiiz72Bq2lwRBx3zxIiaOJnj"

    headers = {
        "Authorization": "Bearer 0q2Jm5XhAiiz72Bq2lwRBx3zxIiaOJnj"
    }

    response3 = requests.get(url, headers=headers)
    data3 = response3.json()
    # Udtag results fra data
    news = data3['results']

    return render(request, 'stocks/detail.html', {'stock': results[0], 'graph': graph, 'price': price, 'news': news})
