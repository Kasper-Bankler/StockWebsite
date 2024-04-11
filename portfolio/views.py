from django.shortcuts import render
from .models import Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Order
from StockWebsite.utils import get_price, API_call
# Create your views here.


@login_required
def index(request, sort=None):

    # Fetch orders fra database
    orders = Order.objects.filter(user=request.user, isActive=True)

    if sort == 'price':
        # sorter orders med price via quicksort
        orders = sorted(orders, key=lambda x: x.stock.price, reverse=True)
    for order in orders:
        price_results = API_call("https://api.polygon.io/v2/aggs/ticker/", order.stock.ticker,
                                 "/range/1/day/2024-01-01/2024-03-01?adjusted=true&sort=asc&limit=120&apiKey=")
        price = get_price(price_results)
        if price is not None:
            order.current_price = price

    return render(request, "index.html", {"orders": orders})


def sell_stock(request, orderID, quantity, price):
    order = get_object_or_404(Order, id=orderID)
    order.isActive = False
    currentUser = request.user
    currentUser.balance = currentUser.balance+quantity*price
    order.save()
    currentUser.save()
    return render(request, "process_sell.html")
