from django.urls import path

from .views import SignUpView
from .views import ProfileView
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView, name="profile")
]
