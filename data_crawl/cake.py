import requests as rq
import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirenorder.settings")
import django
django.setup()
from product.models import *

CSV_PATH = './cake.csv'

with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        print(row)
        Cake.objects.create(
            name = row['name'],
            english_name = row['en_name'],
            img_url = row['img_url'],
            price = row['price'],
            size = row['size'],
            weight = row['weight'],
            description = row['description'],
            category_id = row['category_id'],
            )

