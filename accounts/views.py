from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.shortcuts import render, get_object_or_404
from .models import CustomUser
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def ProfileView(request):
    # Render templaten index.html
    #return render(request, "portfolio/index.html", {"portfolio": top_100_companies}
    return render(request, "profile.html")