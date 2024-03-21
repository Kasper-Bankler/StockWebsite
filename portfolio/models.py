from django.db import models
from stocks.models import Stock
from accounts.models import CustomUser
from django.utils import timezone


# Create your models here.

class Order(models.Model):
    
    quantity = models.IntegerField(max_length=255, default=0)
    transactionDate = models.DateField(auto_now_add=True, auto_now=False)
    isBuyOrder = models.BooleanField(max_length=255, default=True)
    price = models.FloatField(max_length=255, default=0)
    isActive = models.BooleanField(max_length=255, default=True)
    #Hvis en stock slettes, slettes alle stocks i portfolien også
    
    stockID = models.ForeignKey(Stock, on_delete=models.CASCADE)
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        
        return self.stockID
    #def __str__(self):
       # return f"{self.quantity} {self.stock.name} Order by {self.user.username} on {self.transactionDate}"
    
