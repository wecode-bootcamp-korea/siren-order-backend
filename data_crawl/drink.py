import requests as rq
import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirenorder.settings")
import django
django.setup()
from product.models import *

CSV_PATH = './drink.csv'

with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        print(row)
        Drinks.objects.create(
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
            section_id = row['section_id'],
            oz_price = row['oz']
            )

