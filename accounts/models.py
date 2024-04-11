from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
# Vi inheriterer data fra AbstractUser, som er en klasse django har lavet for os,
#  for at få authentication fra brugeren,
# der indeholder hvor mange penge brugeren har


class CustomUser(AbstractUser):
<<<<<<< HEAD

    balance=models.FloatField(default=100000)
    
=======
    balance = models.FloatField(default=100000)

>>>>>>> 8b334d538d9e9003ad4f85fdaac9ed0ecf25855c
    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return self.username
