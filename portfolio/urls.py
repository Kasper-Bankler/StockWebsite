from django.urls import path
from . import views

app_name = 'portfolio'
# Denne liste mapper url endpoints til view funktioner (url configuration)
# Django kalder automatisk funktionerne når siden loades
urlpatterns = [
    path('', views.index, name='index'),
    #path('<str:portfolio_ticker>/', views.detail, name='detail')
]
