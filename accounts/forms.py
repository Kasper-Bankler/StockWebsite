from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

#bruger oprettelse og redigerings former til admin-siden input form taget fra: https://docs.djangoproject.com/en/5.0/topics/auth/customizing/ 


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")
