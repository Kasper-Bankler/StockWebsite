import dataclasses
from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
import requests
from plotly import graph_objects as go
import pandas as pd
from .models import Order
from StockWebsite.utils import quicksort, linear_search
# Create your views here.

@login_required
def index(request, sort=None):

    # Fetch orders from the database
    orders = Order.objects.filter(user=request.user, isActive=True)
    orders = list(orders.values())  # Convert queryset to list of dictionaries

    if sort == 'price':
        # Sort orders by price using quicksort
        quicksort(orders, 0, len(orders) - 1, "price", descending=True)

    return render(request, "index.html", {"orders": orders})
