from django.db import models
from accounts.models import CustomUser
from django.utils import timezone

from stocks.models import Stock


# Create your models here.

class Order(models.Model):
    
    quantity = models.IntegerField(default=0)
    
    
    isBuyOrder = models.BooleanField(max_length=255, default=True)
    
    isActive = models.BooleanField(max_length=255, default=True)
    #Hvis en stock slettes, slettes alle stocks i portfolien også
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    def __str__(self):
        return self.stock.ticker
    #def __str__(self):
       # return f"{self.quantity} {self.stock.name} Order by {self.user.username} on {self.transactionDate}"
    
