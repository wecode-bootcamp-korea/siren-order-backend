import requests as rq
import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirenorder.settings")
import django
django.setup()
from product.models import *

CSV_PATH = './product.csv'

with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        print(row)
        Product.objects.create(
            name = row['name'],
            english_name = row['en_name'],
            img_url = row['img_url'],
            only_ice = row['only_ice'],
            short_price = row['Short'],
            tall_price = row['Tall'],
            grande_price = row['Grande'],
            venti_price = row['Venti'],
            description = row['description'],
            condition = row['condition'],
            oz_price = row['oz'],
            price = row['price'],
            option = row['warming'],
            volume = row['volume'],
            purpose = row['option'],
            size = row['size'],
            weight = row['weight'],
            product_type_id = row['type'], 
            section_id = row['section_id'],
            category_id = row['category_id']
            )

