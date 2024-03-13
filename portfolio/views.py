from django.shortcuts import render
from django.http import HttpResponse
from .models import Orders
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    # Render templaten index.html
    #return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    
    orders = Orders.objects.all
    return render(request, "index2.html", {"portfolio": orders})