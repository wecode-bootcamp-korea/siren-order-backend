import json
import bcrypt
from datetime import datetime

from django.test import Client
from django.test import TestCase
from order.views import *
from order.models import Cart, ProductSize
from account.models import User, Employee, Social
from product.models import Product, Section, Categories, ProductType


class CityModelTest(TestCase):
 
    def setUp(self):
        category = Categories.objects.create(
                       name = '음료'
                   )
        section = Section.objects.create(
                      name = '콜드브루',
                      category = category
                  )
        Product = Product.objects.create(
                     id = 1,
                     name = '돌체 콜드 브루',
                     english_name = 'Dolce Cold Brew',
                     img_url = 'http://image.istarbucks.co.kr/upload/store/skuimg/2019/04/[9200000002081]_20190409153909754.jpg',
                     only_ice = True,
                     oz_price = 0,
                     short_price = 0,
                     tall_price = 5800,
                     grande_price = 6300,
                     venti_price = 6800,
                     description ='무더운 여름철, 동남아 휴가지에서 즐기는 커피를 떠오르게 하는 스타벅스 음료의 베스트 x 베스트 조합인 돌체 콜드 브루를 만나보세요!',
                     condition = '콜드 브루 판매 매장에서만 주문 가능한 음료입니다.',
                     section = section
                )
        social = Social.objects.create(
                     platform = 'normal'
                 )
        bytes_pw = bytes('pass1234', 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        user = User.objects.create(
                   email = 'test@test.net',
                   name = 'test',
                   password = hashed_pw.decode('UTF-8'),
                   gender = '남자',
                   phone_number = '01012341234',
                   social = social,
                   level = 'normal',
               )
        product_type = ProductType.objects.create(
                           id   = 1,
                           name = 'ICED'
                       )
        product_size = ProductSize.objects.create(
                           id   = 5,
                           name = 'venti'
                       )
        options = Options.objects.create(
                      id   = 3,
                      name = '일회용 컵'
                  )    
        Cart.objects.create(
            user = user,
            product_type = product_type,
            product_id = 1,
            product_size = product_size,
            amount = 1,
            options = options,
            price = 6800
        )

    def test_get_cart_with_user(self):
        c = Client()

        test = {'email':'test@test.net', 'password':'pass1234'}
        response = c.post('/account/login', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token'] 
        response = c.get('/order/cart', **{'HTTP_AUTHORIZATION':access_token, 'content_type':'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            [
                {
                    'id'     : 3,
                    'product': '돌체 콜드 브루',
                    'amount' : 1,
                    'price'  : 6800,
                    'options': '일회용 컵',
                    'size'   : 'venti',
                    'type'   : 'ICED'
                }
            ]
        )

    def test_get_without_user(self):
        c = Client()

        response = c.get('/order/cart')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message': '로그인이 필요한 서비스 입니다.',
                'error_code': 'NEED_LOGIN'
            }
        )

    def test_post_cart_with_user(self):
        c = Client()
     
        test = {'email':'test@test.net', 'password':'pass1234'}
        response = c.post('/account/login', json.dumps(test), content_type="application/json")
        data = {
                   'product_type': 1,
                   'product_id': '1', 
                   'amount': '1',
                   'product_size': 5,
                   'options': 3 ,
               }
        access_token = response.json()['access_token'] 
        response = c.post('/order/cart', json.dumps(data), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),{
             'message': 'SUCCESS'
             }
        )

    def test_post_cart_without_user(self):
        c = Client()
        
        data = {
                   'product_type': 1,
                   'product_id': '1', 
                   'amount': '1',
                   'product_size': 5,
                   'options': 3 ,
               }
        response = c.post('/order/cart',json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message': '로그인이 필요한 서비스 입니다.',
                'error_code': 'NEED_LOGIN'
            }
        )

    def test_delete_cart_with_user(self):
        c = Client()

        test = {'email':'test@test.net', 'password':'pass1234'}
        response = c.post('/account/login', json.dumps(test), content_type="application/json")
        data = {
                   'id': 1
               }
        access_token = response.json()['access_token'] 
        response = c.post('/order/cart/delete', json.dumps(data), **{'HTTP_AUTHORIZATION':access_token, 'content_type':"application/json"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message': 'SUCCESS'
            }
        )
                
    def test_delete_cart_without_user(self):
        c = Client()
        
        data = {
                   'id': 1
               }
        response = c.post('/order/cart/delete',json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),
            {
                'message': '로그인이 필요한 서비스 입니다.',
                'error_code': 'NEED_LOGIN'
            }
        )
