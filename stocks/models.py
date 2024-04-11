from datetime import datetime
from django.db import models

# Create your models here.


class Sector(models.Model):
    # Denne klasse gør brug af indkapsling og arv
    name = models.CharField(max_length=255)

    def __str__(self):  # Magic method
        # Navnet af en sektor repræsenteres som en string
        return self.name


class Stock(models.Model):
    transactionDate = models.DateTimeField(default=datetime.now())
<<<<<<< HEAD
    ticker = models.CharField(max_length=255,default='')
    
    # Hvis en sector slettes, slettes alle aktier i den også
    price = models.FloatField(max_length=255,default=0.0)
    
 
=======
    ticker = models.CharField(max_length=255, default='')
    price = models.FloatField(max_length=255, default=0.0)
>>>>>>> 8b334d538d9e9003ad4f85fdaac9ed0ecf25855c

    def save(self, *args, **kwargs):
        self.transactionDate = datetime.now().replace(second=0, microsecond=0)
        super(Stock, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('ticker', 'price', 'transactionDate')

    def __str__(self):
        return self.ticker
