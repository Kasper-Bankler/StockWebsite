from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


#Denne view er klasse baseret istedet for det almindelige funktionsbaseret view. Taget fra følgende kilde: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Authentication 
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def ProfileView(request):

    #brugerens saldo bliver rundet op til 2 decimaler
    balance = round(request.user.balance, 2)

    return render(request, "profile.html", {'bal': balance})
