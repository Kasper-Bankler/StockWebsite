from django.contrib import admin
from .models import Sector, Stock


class SectorAdmin(admin.ModelAdmin):
    # Denne klasse viser id og navn på admin siden
    list_display = ('id', 'name')


class StockAdmin(admin.ModelAdmin):
    # Denne klasse viser id, navn og ticker på admin siden
    list_display = ('price', 'ticker', 'transactionDate')


# Register your models here.
admin.site.register(Sector, SectorAdmin)
admin.site.register(Stock, StockAdmin)
