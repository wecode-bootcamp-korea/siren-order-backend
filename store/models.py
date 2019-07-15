from django.db import models

class City(models.Model):
    city_code = models.IntegerField(max_length=3)
    city_name = models.CharField(max_length=50)

    class META:
        db_table = "city"

class Gungu(models.Model):
    gungu_code = models.IntegerField(max_length=5)
    gungu_name = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
    class META:
        db_table = "gungu"

class Store(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    gungu = models.ForeignKey(Gungu, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    fax_number = models.CharField(max_length=20)
    opened_at = models.CharField(max_length=8)
    lat = models.DecimalField(max_digits=13,decimal_places=10)
    lng = models.DecimalField(max_digits=13,decimal_places=10)

    class META:
        db_table = "store"
