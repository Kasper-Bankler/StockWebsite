from django.db import models

# Create your models here.


class Sector(models.Model):
    # Denne klasse gør brug af indkapsling og arv
    name = models.CharField(max_length=255)

    def __str__(self):  # Magic method
        # Navnet af en sektor repræsenteres som en string
        return self.name


class Stock(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=255)
    # Hvis en sector slettes, slettes alle aktier i den også
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
