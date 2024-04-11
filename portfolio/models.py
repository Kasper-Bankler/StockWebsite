from django.db import models
from accounts.models import CustomUser
from stocks.models import Stock


# Create your models here.

class Order(models.Model):

    quantity = models.IntegerField(default=0)

    isActive = models.BooleanField(max_length=255, default=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Hvis en stock slettes, slettes alle stocks i portfolien også
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return self.stock.ticker
