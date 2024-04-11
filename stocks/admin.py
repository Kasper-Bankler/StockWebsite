from django.contrib import admin
from .models import Sector, Stock


class SectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    # Viser id og navn for sektorobjekter i admin-interfacet


class StockAdmin(admin.ModelAdmin):
    list_display = ('price', 'ticker', 'transactionDate')
    # Viser pris, ticker og transaktionsdato for aktieobjekter i admin-interfacet


# Registrerer modellerne til admin
admin.site.register(Sector, SectorAdmin)
admin.site.register(Stock, StockAdmin)
