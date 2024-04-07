from django.db import models

# Create your models here.


class Sector(models.Model):
    # Denne klasse gør brug af indkapsling og arv
    name = models.CharField(max_length=255)

    def __str__(self):  # Magic method
        # Navnet af en sektor repræsenteres som en string
        return self.name


class Stock(models.Model):
    transactionDate = models.DateTimeField(auto_now_add=True, auto_now=False)
    ticker = models.CharField(max_length=255,default='')
    # Hvis en sector slettes, slettes alle aktier i den også
    price = models.FloatField(max_length=255,default=0.0)
    
    def clean_transactionDate(self):
        data = self.cleaned_data['transactionDate']
    # do some stuff
        data.replace(microsecond=0,second=0)
        return data

    class Meta:
        unique_together = ('ticker', 'price', 'transactionDate')

    def __str__(self):
        return self.ticker

   
