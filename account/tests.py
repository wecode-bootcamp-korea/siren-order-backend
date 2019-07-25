import json
import bcrypt
from datetime import datetime

from account.models import User, Social, Employee
from store.models import City, Gungu, Store
from django.test import TestCase
from django.test import Client
from unittest.mock import patch, MagicMock

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
                    "user_name"    : user.name,
                    "email"        : user.email
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

    def test_user_change_password_check(self):
        c = Client()

        test         = {'email' : 'test@gmail.com',"password":"1234"}
        response     = c.post('/account/login', json.dumps(test), content_type='applications/json')
        access_token = response.json()["access_token"]

        test ={"current_password": "1234", "new_password" :"5678"}
        response = c.post("/account/login/chpw", json.dumps(test), **{"HTTP_AUTHORIZATION":access_token, "content_type" : "application/json"})

        self.assertEqual(response.status_code, 200)

class EmployeeTest(TestCase):
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
        store = Store.objects.create(
            id         = 1,
            name       = '도산 가로수 길',
            address    = '서울특별시 강남구 논현동 5번지 2층',
            telephone  = '02-758-8429',
            fax_number = '02-514-8429',
            opened_at  = '20110907',
            lat        = 37.5173623000,
            lng        = 127.0232957000,
            city       = city,
            gungu      = gungu
        )
        bytes_pw = bytes('1234', 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        Employee.objects.create(
            name          = '아이유',
            employee_code = '100011',
            password      = hashed_pw.decode('UTF-8'),
            phone_number  = '010-1234-1111',
            city          = '서울',
            gungu         = '강남구',
            grade         = '매니저',
            store         = store
        )

    def tearDown(self):
        Employee.objects.filter(name='아이유').delete()

    def test_employee_account_check(self):
        c = Client()

        test     = {'name': '제니', 'employee_code':'00010131', 'password':'pass1234', 'phone_number':'010-1111-1234','city':'서울','gungu':'강남구', 'grade':'매니저', 'store_id':1}
        response = c.post('/account/employee', json.dumps(test), content_type='applications/json')
        self.assertEqual(response.status_code, 200)

    def test_employee_account_code_check(self):
        c = Client()

        test     = {'name': '나나', 'employee_code':'100011', 'password':'1234', 'phone_number':'01012345678','city':'서울','gungu':'강남구', 'grade':'지점장', 'store_id':1}
        response = c.post('/account/employee', json.dumps(test), content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'EMPLOYEE_CODE_EXIST'})

    def test_employee_login_check(self):
        c = Client()

        test     = {'employee_code':'100011', 'password':'1234'}
        employee = Employee.objects.get(employee_code=test['employee_code'])
        response = c.post('/account/employee/login', json.dumps(test), content_type="application/json")
        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    "access_token" : access_token,
                    "name" : employee.name
                })

    def test_employee_login_code_check(self):
        c = Client()

        test     = {'employee_code':'00010301', 'password':'1234'}
        response = c.post('/account/employee/login', json.dumps(test), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_EMPLOYEE'})

    def test_user_login_password_check(self):
        c = Client()

        test     = {'employee_code':'100011', 'password':'12345'}
        response = c.post('/account/employee/login', json.dumps(test), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'INVALID_PASSWORD'})

    @patch("account.views.requests")
    def test_employee_kakao_account(self, mocked_requests):
        c = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id" : "12345",
                    "properties" : {
                        "nickname" : "아이유"
                    }
                }

        mocked_requests.post = MagicMock(return_value = MockedResponse())

        test = {
            'employee_code':'1000111',
            'password':'1234',
            'nickname' : '아이유'
        }

        response = c.post("/account/employee/kakao", json.dumps(test), **{"HTTP_AUTHORIZATION":"1234","content_type" : "application/json"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    'message' : 'SUCCESS'
                }
        )

