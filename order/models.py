from django.db import models
from account.models import User, Employee
from product.models import Product, ProductType
from store.models import Store 


class ProductSize(models.Model):
    name = models.CharField(max_length=6)

    class Meta:
        db_table='product_size'

class Options(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table='options' 

class Orders(models.Model):
    user  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.IntegerField(default=0)
    product_size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=0)    
    options = models.ForeignKey(Options, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=1)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='orders'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True)
    options = models.CharField(max_length=50)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='cart'

class Process(models.Model):
    orders = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True)
    is_offer = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='process'

class History(models.Model):
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    orders = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='history'
      
