from django.db import models
from stocks.models import Stock

# Create your models here.

class Portfolio(models.Model):
    userID = models.CharField(max_length=255)
    stockID = models.CharField(max_length=255)
    # Hvis en sector slettes, slettes alle aktier i den også
    quantity = models.IntegerField(max_length=255)
    buyingPrice = models.IntegerField(max_length=255)

    #Hvis en stock slettes, slettes alle stocks i portfolien også
    Stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
