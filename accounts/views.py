from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import get_list_or_404, render
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from portfolio.models import Order


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def ProfileView(request):
    
    stocks = list(Order.objects.filter(userID=request.user.id))
    if not stocks:
        stocks=[{'ticker':"no stocks",'quantity':0}]
    return render(request, "profile.html",{'stocks':stocks})