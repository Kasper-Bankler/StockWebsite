from datetime import datetime
from django.db import models



class Stock(models.Model):
    # Dette er en model til at repræsentere aktier.
    transactionDate = models.DateTimeField(default=datetime.now())
    ticker = models.CharField(max_length=255, default='')
    price = models.FloatField(max_length=255, default=0.0)

    def save(self, *args, **kwargs):
        # Transaktions datoen opdateres
        self.transactionDate = datetime.now().replace(second=0, microsecond=0)
        # Her kaldes den oprindelige .save funktion for at opdatere databasen.
        super(Stock, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('ticker', 'price', 'transactionDate')
        # Definerer et unikt sammenhængende sæt af felter bestående af ticker, pris og transaktionsdato.

    def __str__(self):
        return self.ticker
        # Returnerer ticker-symbolet som strengrepræsentation af Stock-objektet.
