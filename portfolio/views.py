from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    # Render templaten index.html
    #return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    
    orders = Order.objects.all #Henter alt data fra orders i databasen
    return render(request, "index2.html", {"orders": orders})