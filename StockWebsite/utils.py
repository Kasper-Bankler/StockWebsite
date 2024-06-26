import requests
from plotly import graph_objects as go
import pandas as pd
from .settings import apiKeys


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


# Inspireret af geeksforgeeks https://www.geeksforgeeks.org/quick-sort/
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

# Inspiration fra geeksforgeeks https://www.geeksforgeeks.org/linear-search/


def linear_search(tickers, target):
    for ticker in tickers:
        if ticker['T'] == target:
            return ticker
    return -1


def API_call(url1, stockTicker="", url2=""): #Lav HTTP GET REQUEST til API og returner resultat
    # increment counter
    API_call.counter += 1

    # Vælg API-nøgle baseret på counter
    apiKey=apiKeys[API_call.counter%len(apiKeys)]

    # Opsæt headers med api key
    headers = {
        "Authorization": "Bearer "+apiKey
    }

    # Konstruer API-opkaldets URL og foretag anmodning
    if (stockTicker != ""):
        callUrl = url1+stockTicker+url2+apiKey
        response = requests.get(callUrl, headers=headers)
    else:
        callUrl = url1+apiKey
        response = requests.get(callUrl, headers=headers)

    # Konverter respons til JSON-format og returner resultatet
    data = response.json()
    return (data['results'])


# Initialiser  API-opkald counter
API_call.counter = 0


def create_graph(graph_data):

    # Opret tomme lister til at gemme dataene
    closeList = []
    openList = []
    highList = []
    lowList = []
    timeList = []

    # Loop gennem dataene og adskil dem i de forskellige lister baseret på kategori
    for bar in graph_data:
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

    # Opret en figur og tilføj Candlestick-grafen
    # https://plotly.com/python/candlestick-charts/
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=times, open=openList,
                  high=highList, low=lowList, close=closeList, name='graph'))
    fig.update_layout(xaxis_rangeslider_visible=False)

    # Konverter figuren til HTML og returner både grafen og den seneste pris
    graph = fig.to_html()
    return graph, price


def get_price(data):
    # Funktion til at hente den seneste lukkepris fra data.
    closeList = []
    for price in data:
        for category in price:
            if category == 'c':
                closeList.append(price[category])
    return closeList[-1]


def get_name_and_ticker(data):
    # Funktion til at hente navn og ticker fra data.
    name = data['name']
    ticker = data['ticker']
    return name, ticker
