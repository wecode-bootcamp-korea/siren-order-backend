from django.db import models

class City(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "city"

class Gungu(models.Model):
    code = models.CharField(max_length=5)
    name = models.CharField(max_length=50, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = "gungu"

class Store(models.Model):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    gungu = models.ForeignKey(Gungu, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=2500, null=True)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20)
    opened_at = models.CharField(max_length=8)
    lat = models.DecimalField(max_digits=13,decimal_places=10)
    lng = models.DecimalField(max_digits=13,decimal_places=10)

    class Meta:
        db_table = "store"
