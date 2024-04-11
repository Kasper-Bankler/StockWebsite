from django.shortcuts import render
from StockWebsite.utils import API_call, create_graph


def home(request):
    # Henter grafdata fra Polygon API for spy tickeren for en given periode
    graph_data = API_call("https://api.polygon.io/v2/aggs/ticker/", "SPY",
                          "/range/1/day/2000-01-01/2024-03-01?adjusted=true&sort=asc&limit=10000&apiKey=")

    # Opretter grafen og henter prisen fra grafdataene
    graph, price = create_graph(graph_data)

    # Henter de seneste nyheder om SPY
    news = API_call(
        "https://api.polygon.io/v2/reference/news?ticker=", "SPY", "&limit=3&apiKey=")

    # Returnerer renderingen af hjemmesiden med grafen og nyhederne
    return render(request, 'home.html', {'graph': graph, 'news': news})
