from django.contrib import admin
from .models import Order



class OrderAdmin(admin.ModelAdmin):
    # Denne klasse viser id, navn og ticker på admin siden
    list_display = ('stock', 'user', 'isActive','quantity')


# Register your models here.
admin.site.register(Order, OrderAdmin)