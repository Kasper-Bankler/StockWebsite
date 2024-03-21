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
# Create your views here.


@login_required
def index(request, sort=None):
    # Render templaten index.html
    # return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    orders = list(Order.objects.filter(userID=request.user.id))  # Henter alt data fra orders i databasen


    # Render templaten index.html
    
    return render(request, "index.html", {"orders": orders})
