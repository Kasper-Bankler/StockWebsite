from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    #app_label = "accounts"
    balance=models.FloatField(default=100000)
    
    def __str__(self):
        return self.username
    
    class Meta:
        app_label = 'accounts' 