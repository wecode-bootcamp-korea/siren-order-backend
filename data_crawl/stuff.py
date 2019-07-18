import requests as rq
import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirenorder.settings")
import django
django.setup()
from product.models import *

CSV_PATH = './stuff.csv'

with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        print(row)
        Stuff.objects.create(
            name = row['name'],
            english_name = row['en_name'],
            img_url = row['img_url'],
            price = row['price'],
            volume = row['volume'],
            option = row['option'],
            description = row['description'],
            condition = row['condition'],
            section_id = row['section_id']
            )

