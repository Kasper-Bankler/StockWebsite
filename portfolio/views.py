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
# Create your views here.


@login_required
def index(request):
    # Render templaten index.html
    # return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    orders = list(Order.objects.filter(user=request.user,isActive=True))  # Henter alt data fra orders i databasen

    #fetch = Order.objects.all() #Dette henter alt data fra order databasen

    #return render(request, "index.html",
             #     {"fetch": fetch})

    # Render templaten index.html
    
    return render(request, "index.html", {"orders": orders})
