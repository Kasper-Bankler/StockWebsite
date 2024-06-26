from django.contrib import admin
from .models import  Stock



class StockAdmin(admin.ModelAdmin):
    list_display = ('price', 'ticker', 'transactionDate')
    # Viser pris, ticker og transaktionsdato for aktieobjekter i admin-interfacet


# Registrerer modellerne til admin
admin.site.register(Stock, StockAdmin)
