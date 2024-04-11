from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def ProfileView(request):

    balance = round(request.user.balance, 2)

    return render(request, "profile.html", {'bal': balance})
