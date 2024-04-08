from django.urls import path, register_converter
from . import converters, views

register_converter(converters.FloatUrlParameterConverter, 'float')

app_name = 'stocks'
# Denne liste mapper url endpoints til view funktioner (url configuration)
# Django kalder automatisk funktionerne når siden loades
urlpatterns = [
    path('', views.index, name='index'),
    path('sort-<str:sort>/', views.index, name='index'),
    path('search-<str:search>/', views.index, name='index'),
    path('<str:stock_ticker>/', views.detail, name='detail'),
    path('<str:stock_ticker>/<str:transaction_type>', views.handle_transaction, name='handle_transaction'),
    
    path('<str:stock_ticker>/<int:quantity>/<float:price>/process',
         views.process, name='process'),
    path("redirecting", views.redirect, name = "redirect"),
]
