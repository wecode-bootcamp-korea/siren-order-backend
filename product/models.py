from django.db import models

class Categories(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'categories'

class Section(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    class Meta:
        db_table = 'section'

class ProductType(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'product_type'

class Product(models.Model):
    name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=450) 
    only_ice = models.BooleanField(default=True)
    oz_price = models.IntegerField(default=0, null=True, blank=True)
    short_price = models.IntegerField(default=0, null=True, blank=True)
    tall_price = models.IntegerField(default=0, null=True, blank=True)
    grande_price = models.IntegerField(default=0, null=True, blank=True)
    venti_price = models.IntegerField(default=0, null=True, blank=True)
    description = models.CharField(max_length=400, null=True)
    condition = models.CharField(max_length=200, null=True)
    price = models.IntegerField(default=0, null=True, blank=True)
    volume = models.CharField(max_length=4)
    option = models.CharField(max_length=20, null=True)
    purpose = models.CharField(max_length=30, null=True)
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)  
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'product'

    def get_price(self, size):
    
        SIZE_ORDER={
            "7oz"   : self.oz_price,
            "short" : self.short_price,
            "tall"  : self.tall_price,
            "grande": self.grande_price,
            "venti" : self.venti_price
        }
        return SIZE_ORDER[size]    
  
class Hot(models.Model):
    name = models.CharField(max_length=50)
    english_name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=450)
    description = models.CharField(max_length=400, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'hot'

