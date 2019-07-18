import json
from django.test import Client
from django.test import TestCase
from store.views import *
from store.models import *

class CityModelTest(TestCase):
 
    def setUp(self):
        city = City.objects.create(
                     id = 1,
                   name = "서울",
                   code = "01",
               )
        gungu = Gungu.objects.create(
              id = 1,
            code = "0101",
            name = "강남구",
            city = city
        )
        Store.objects.create(
            address = "서울특별시 강남구 논현동 5번지 2층",
            city = city,
            fax_number = "02-514-8429",
            gungu = gungu,
            id =  1,
            lat = "37.5173623000",
            lng = "127.0232957000",
            name =  "도산가로수길",
            opened_at = "20110907",
            telephone = "02-758-8429"
        )

    def test_get_sido(self):
        c = Client()

        response = c.get("/store/sido")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                [
                    {   
                        "code": "01",
                        "id": 1,
                        "name": "서울",
                    }
                ]
                  
        )

    def test_get_shop(self):
        c = Client()

        response = c.get("/store/sido/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                [
                    {
                        'id': 1,
                        'city_id': 1,
                        'gungu_id': 1,
                        'name': '도산가로수길',
                        'address': '서울특별시 강남구 논현동 5번지 2층',
                        'telephone': '02-758-8429', 
                        'fax_number': '02-514-8429',
                        'opened_at': '20110907',
                        'lat': '37.5173623000',
                        'lng': '127.0232957000'
                    }
               ]
        )

    def test_get_gungu(self):
        c = Client()

        response = c.get("/store/gungu/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
               [
                   {
                       'id': 1,
                     'code': '0101',
                     'name': '강남구',
                  'city_id': 1
                   }
               ]
        )    

    def test_get_store(self):
        c = Client()

        response = c.get("/store/shop/1")
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(
            response.json(),
                [
                    {
                        'id': 1,
                        'city_id': 1,
                        'gungu_id': 1,
                        'name': '도산가로수길',
                        'address': '서울특별시 강남구 논현동 5번지 2층',
                        'telephone': '02-758-8429', 
                        'fax_number': '02-514-8429',
                        'opened_at': '20110907',
                        'lat': '37.5173623000',
                        'lng': '127.0232957000'
                    }
               ]
       )
