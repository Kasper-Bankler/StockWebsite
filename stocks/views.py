from django.shortcuts import render
from datetime import datetime

# Importering af hjælpefunktioner og modeller
from StockWebsite.utils import API_call, quicksort, linear_search, create_graph, get_name_and_ticker, get_price
from portfolio.models import Order
from .models import Stock
from django.contrib.auth.decorators import login_required

# Opret dine views her.


def index(request, sort="", search=""):
    # Funktion for hovedsiden der kaldes når siden indlæses

    # API-kald for at hente data
    results = API_call(
        "https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2024-03-06?adjusted=true&apiKey=")

    # Sorter listen baseret på handelsvolumen ('v')
    sorted_results = quicksort(
        results, 0, len(results)-1, 'v', descending=True)

    # Vælg de 100 mest handlede aktier
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

    # Retunerer skabelonen index.html
    return render(request, "stocks/index.html", {"stocks": stocks})


def detail(request, stock_ticker):
    # Detaljefunktion

    # API-anmodning for at hente data om aktien
    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")

    # API-anmodning for at hente grafdata
    graph_data = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                          "/range/1/day/2024-01-01/2024-04-01?adjusted=true&sort=asc&limit=120&apiKey=")

    # Opret graf og hent pris
    graph, price = create_graph(graph_data)

    # API-anmodning for at hente nyheder om aktien
    news = API_call(
        "https://api.polygon.io/v2/reference/news?ticker=", stock_ticker, "&limit=3&apiKey=")

    return render(request, 'stocks/detail.html', {'stock': ticker_results, 'graph': graph, 'price': price, 'news': news})


@login_required
def process(request, stock_ticker, quantity, price):
    # Funktion til at behandle en handel

    # Beregn prisen
    cost = quantity * price

    # Opret eller hent aktieobjekt fra databasen
    stock_obj, created = Stock.objects.get_or_create(
        price=price,
        ticker=stock_ticker,
        transactionDate=datetime.now().replace(second=0, microsecond=0)
    )

    # Opret en handelsordre
    order_obj = Order(quantity=quantity, user=request.user, stock=stock_obj)

    # Opdater brugerens saldo
    currentUser = request.user
    currentUser.balance = currentUser.balance-cost

    # Gem ændringerne i databasen
    order_obj.save()
    currentUser.save()

    return render(request, 'stocks/process_trade.html', {'stockTicker': stock_ticker, 'quantity': quantity, 'price': price})


@login_required
def handle_transaction(request, stock_ticker):
    # Funktion til at håndtere en transaktion

    # API-anmodning for at hente prisdata
    price_results = API_call("https://api.polygon.io/v2/aggs/ticker/", stock_ticker,
                             "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")

    # API-anmodning for at hente data om aktien
    ticker_results = API_call(
        "https://api.polygon.io/v3/reference/tickers/", stock_ticker, "?apiKey=")

    # Hent pris og navn på aktien
    price = get_price(price_results)
    name, ticker = get_name_and_ticker(ticker_results)

    # Hent brugerens saldo
    balance = round(request.user.balance, 2)

    return render(request, 'stocks/handle_transaction.html', {'price': price, 'name': name, 'ticker': ticker, 'bal': balance})
