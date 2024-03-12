from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # Render templaten index.html
    #return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    return HttpResponse("Hello world")