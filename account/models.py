from django.db import models
from store.models import Store

class Social(models.Model):
    platform = models.CharField(max_length=30, default="normal")

    class Meta:
        db_table = "social"

class User(models.Model):
    email           = models.EmailField(max_length=100, unique=True, null=True)
    name            = models.CharField(max_length=50)
    password        = models.CharField(max_length=100, null=True)
    gender          = models.CharField(max_length=10)
    phone_number    = models.CharField(max_length=50, null=True)
    social          = models.ForeignKey(Social, max_length=10, on_delete=models.SET_NULL, null=True, default=None)
    social_login_id = models.CharField(max_length=100, null=True)
    level           = models.CharField(max_length=20, default="normal")
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user"

class Employee(models.Model):
    name           = models.CharField(max_length=50)
    employee_code  = models.CharField(max_length=100, unique=True) 
    password       = models.CharField(max_length=100)
    phone_number   = models.CharField(max_length=50)
    grade          = models.CharField(max_length=30)
    city           = models.CharField(max_length=10, null=True)
    gungu          = models.CharField(max_length=20, null=True)
    store          = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True, default=None)
    kakao_id       = models.CharField(max_length=50, null=True)
    created_at     = models.DateTimeField(auto_now_add=True) 
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "employee"

class Login(models.Model):
    logined_at = models.DateTimeField(auto_now=True)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    employee   = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "login"
