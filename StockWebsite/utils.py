import requests
from plotly import graph_objects as go
import pandas as pd
from .settings import apiKey1, apiKey2, apiKey3


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


def API_call(url1, stockTicker="", url2=""):
    API_call.counter += 1

    if API_call.counter % 3 == 0:
        apiKey = apiKey1
    elif API_call.counter % 3 == 1:
        apiKey = apiKey2
    else:
        apiKey = apiKey3

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


API_call.counter = 0


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
