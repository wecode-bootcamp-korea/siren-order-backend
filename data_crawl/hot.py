import requests as rq
import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirenorder.settings")
import django
django.setup()
from product.models import *

CSV_PATH = './hot.csv'

with open(CSV_PATH, newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    for row in spamreader:
        print(row)
        Hot.objects.create(
            name = row['name'],
            english_name = row['en_name'],
            img_url = row['img_url'],
            description = row['description'],
            drink_id = row['drink_id']
            )

