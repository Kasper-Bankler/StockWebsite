from django.urls import path
from . import views


# Denne liste mapper url endpoints til view funktioner (url configuration)
# Django kalder automatisk funktionerne når siden loades
urlpatterns = [
    path('', views.index, name='index')
]
