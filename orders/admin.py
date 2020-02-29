from django.contrib import admin
from .models import Pizza, Topping, Dinner, Salad, Pasta, Sub, Cart, Order

# Register your models here.
admin.site.register(Pizza)
admin.site.register(Topping)
admin.site.register(Dinner)
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(Sub)
admin.site.register(Cart)
admin.site.register(Order)