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

class Drinks(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=450) 
    only_ice = models.BooleanField(default=True)
    oz_price = models.CharField(max_length=10, null=True)
    short_price = models.CharField(max_length=10, null=True)
    tall_price = models.CharField(max_length=10, null=True)
    grande_price = models.CharField(max_length=10, null=True)
    venti_price = models.CharField(max_length=10, null=True)
    description = models.CharField(max_length=400, null=True)
    condition = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)   

    class Meta:
        db_table = 'drinks'

class Hot(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=450)
    description = models.CharField(max_length=400, null=True)
    drink = models.ForeignKey(Drinks, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'hot'

class Foods(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=450)
    price = models.CharField(max_length=10)
    description = models.CharField(max_length=400, null=True)
    condition = models.CharField(max_length=200, null=True)
    option = models.BooleanField(default=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)   

    class Meta:
        db_table = 'foods'

class Stuff(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=450)
    price = models.CharField(max_length=10)
    volume = models.CharField(max_length=4)
    option = models.CharField(max_length=20, null=True)
    description = models.CharField(max_length=400, null=True)
    condition = models.CharField(max_length=200, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)   

    class Meta:
        db_table = 'stuff'

class Cake(models.Model):
    name = models.CharField(max_length=50)
    en_name = models.CharField(max_length=50)
    img_url = models.CharField(max_length=450)
    price = models.CharField(max_length=10)
    size = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    description = models.CharField(max_length=400, null=True)
    condition = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)  

    class Meta:
        db_table = 'cake' 
