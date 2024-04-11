from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
# CustomUser arver fra Djangos indbyggede AbstractUser model

# der indeholder hvor mange penge brugeren har


class CustomUser(AbstractUser):
    #Der tilføjes et felt som er brugerens saldo
    balance = models.FloatField(default=100000)

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.username
