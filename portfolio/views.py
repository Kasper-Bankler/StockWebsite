from django.shortcuts import render
from django.http import HttpResponse
from .models import Portfolio

# Create your views here.
def index(request):
    # Render templaten index.html
    #return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    portfolio = Portfolio.objects.all
    return render(request, "index2.html", {"portfolio": Portfolio})