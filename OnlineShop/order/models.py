from django.db import models
from django.contrib.auth.models import User
from product.models import Product
from product.models import Variants

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('Shipping', 'Shipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    CITIES = (
        ('Almaty','Almaty'),
        ('Astana','Astana'),
        ('Shimkent','Shimkent'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=60,choices=CITIES, default='Astana')
    country = models.CharField(max_length=60)
    total = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=300)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username}'s order"


class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('Shipping', 'Shipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    adminnote = models.CharField(blank=True, max_length=300)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'order of {self.product.title}'





class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    variant = models.ForeignKey(Variants, on_delete=models.SET_NULL,null=True, blank=True)
    @property
    def price(self):
        return self.product.price

    @property
    def amount(self):
        if self.variant != None:
            return self.quantity * self.variant.price
        else:
            return self.quantity * self.product.price

    @property
    def veramount(self):
        return self.quantity*self.variant.price