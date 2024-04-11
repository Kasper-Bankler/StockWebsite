from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Brugerformular til oprettelse af brugere
    add_form = CustomUserCreationForm
    # Brugerformular til redigering af brugere
    form = CustomUserChangeForm
    # Brugermodel, der administreres af denne adminklasse
    model = CustomUser
    # Liste over felter, der vises i adminpanelet
    list_display = ["email", "username", "balance"]


# Registrerer CustomUser-modellen med dens adminklasse
admin.site.register(CustomUser, CustomUserAdmin)