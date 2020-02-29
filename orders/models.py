from django.db import models

class Topping(models.Model):
    name = models.CharField(max_length=70)

    def __str__(self):
        return self.name
        
class Pizza(models.Model):
    name = models.CharField(max_length=100)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)
    toppings_no = models.IntegerField()
    toppings= models.ManyToManyField(Topping)

    def __str__(self):
        return f"{self.name} small price {self.small_price} large price  {self.large_price} has {self.toppings_no} toppings "

class Dinner(models.Model):
    name = models.CharField(max_length=150)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} small price {self.small_price} and large price {self.large_price}.'

class Salad(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} price is ${self.price}' 

class Pasta(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.name} price is ${self.price}'          

class Sub(models.Model):
    name = models.CharField(max_length=100)
    small_price = models.DecimalField(max_digits=6, decimal_places=2)
    large_price = models.DecimalField(max_digits=6, decimal_places=2)
    toppings_no = models.IntegerField()
    toppings= models.ManyToManyField(Topping)

    def __str__(self):
        return f"{self.name} small price {self.small_price} large price  {self.large_price} has {self.toppings_no} toppings "

class Cart(models.Model):
    user_id = models.IntegerField()
    order_contents = models.TextField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    user_name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user_id} {self.user_name} added {self.order_contents} worth of {self.total_price}' 

class Order(models.Model):
    user_id = models.IntegerField()
    order_price = models.DecimalField(max_digits=8, decimal_places=2) 
    order_details = models.TextField()
    user_name = models.CharField(max_length=200)
    o_status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id} {self.user_name} placed {self.order_details} worth of {self.order_price}'       
# Create your models here.
