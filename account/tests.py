import unittest
import json
import bcrypt
from datetime import datetime

from account.models import User,Social
from django.test import TestCase
from django.test import Client


class UserTest(TestCase):
    def setUp(self):
        social = Social.objects.create(
            platform = 'normal'
        )
        bytes_pw = bytes('1234', 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        User.objects.create(
            email='test@gmail.com',
            name='test',
            password= hashed_pw.decode('UTF-8'),
            phone_number='01012345678',
            gender='남자',
            social = social
        )

    def tearDown(self):
        User.objects.filter(name='test').delete()

    def test_user_account_check(self):
        c = Client()

        test     = {'email': 'test1@gmail.com', 'name':'test1', 'password':'5678', 'phone_number':'01087654321', 'gender':'여자'}
        response = c.post('/account', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 200)

    def test_user_account_email_check(self):
        c = Client()

        test     = {'email': 'test@gmail.com', 'name':'test', 'password':'1234', 'phone_number':'01012345678'}
        response = c.post('/account', json.dumps(test), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'DUPLICATE_EMAIL'})

    def test_user_account_phone_number_check(self):
        c = Client()

        test     = {'email': 'test2@gmail.com', 'name':'test', 'password':'1234', 'phone_number':'01012345678'}
        response = c.post('/account', json.dumps(test), content_type="applications/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'DUPLICATE_PHONE_NUMBER'})

    def test_user_login_check(self):
        c = Client()

        test     = {'email':'test@gmail.com', 'password':'1234'}
        user     = User.objects.get(email=test['email'])
        response = c.post('/account/login', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    "access_token" : access_token,
                    "user_name"    : user.name
                })

    def test_user_login_email_check(self):
        c = Client()

        test     = {'email':'tes@gmail.com', 'password':'1234'}
        response = c.post('/account/login', json.dumps(test), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_EMAIL'})

    def test_user_login_password_check(self):
        c = Client()

        test     = {'email':'test@gmail.com', 'password':'12345'}
        response = c.post('/account/login', json.dumps(test), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_PASSWORD'})


