from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
 # Vi inheriterer data fra AbstractUser, som er en klasse django har lavet for os, 
 #  for at få authentication fra brugeren,
 # der indeholder hvor mange penge brugeren har
class CustomUser(AbstractUser):
    #app_label = "accounts"
    balance=models.FloatField(default=100000)
    # groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    # user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')    
    class Meta:
        app_label = 'accounts' 