import json
import bcrypt
import jwt
import requests

from account.models      import User, Social, Login, Employee
from store.models        import City, Gungu, Store
from django.views        import View
from django.http         import JsonResponse
from datetime            import datetime
from sirenorder.settings import SECRET_KEY, EXP_TIME

class AccountView(View):

    def post(self, request):
        new_user_info = json.loads(request.body)

        if User.objects.filter(email = new_user_info['email']).exists():
            return JsonResponse(
                {'message' : 'DUPLICATE_EMAIL'},
                status = 400
            )

        if User.objects.filter(phone_number = new_user_info['phone_number']).exists():
            return JsonResponse(
                {'message' : 'DUPLICATE_PHONE_NUMBER'},
                status = 400
            )

        bytes_pw  = bytes(new_user_info['password'], 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())

        user_info = User(
            email        = new_user_info['email'],
            password     = hashed_pw.decode('UTF-8'),
            name         = new_user_info['name'],
            phone_number = new_user_info['phone_number'],
        )
        user_info.save()

        return JsonResponse(
            {'message':'SUCCESS'},
            status=200
        )

class LoginView(View):

    def post(self, request):
        login_user_info = json.loads(request.body)
        siren_secret = SECRET_KEY
        exp_time = EXP_TIME
       
        try:
            user = User.objects.get(email=login_user_info['email'])
        except User.DoesNotExist:
            return JsonResponse(
                {'message' : 'INVALID_EMAIL'},
                status = 400
            )

        if bcrypt.checkpw(login_user_info['password'].encode('UTF-8'), user.password.encode('UTF-8')):
            jwt_token = jwt.encode({'id':user.id, 'exp':exp_time}, siren_secret, algorithm='HS256')

            login_check = Login(
                user = User.objects.get(email=user.email),
            )
            login_check.save()

            return JsonResponse({
                    'access_token' : jwt_token.decode('UTF-8'),
                    'user_name'    : user.name
                }, status = 200
            )
        else:
            return JsonResponse(
                {'message': 'INVALID_PASSWORD'},
                status = 400
            )

class EmployeeSignup(View):

    def post(self, request):
        data = json.loads(request.body)

        if Employee.objects.filter(employee_code = data["employee_code"]).exists():
            return JsonResponse(
                {"message" : "EMPLOYEE_CODE_EXIST"},
                status=400
            )
        else:        
            password = bytes(data["password"], "utf-8")
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
       
            new_employee = Employee(
                name = data["name"],
                password = hashed_password.decode("utf-8"),
                employee_code = data["employee_code"],
                city = data["city"],
                gungu = data["gungu"],
                phone_number = data["phone_number"],
                grade = data["grade"],
                store_id = data["store_id"]
            )
            new_employee.save()

            return JsonResponse(
                {"message" : "SUCCESS"},
                status=200
            )

class EmployeeLogin(View):

    def post(self, request):
        login_employee = json.loads(request.body)
        siren_secret = SECRET_KEY
        exp_time = EXP_TIME

        if Employee.objects.filter(employee_code = login_employee["employee_code"]).exists():
            employee_data = Employee.objects.get(employee_code=login_employee["employee_code"])
        else:
            return JsonResponse(
                {"message": "INVALID_EMPLOYEE"},
                status=400
            )

        if bcrypt.checkpw(login_employee["password"].encode("utf-8"), employee_data.password.encode("utf-8")):
            encoded_jwt = jwt.encode({"user_id":employee_data.id, 'exp':exp_time}, siren_secret, algorithm="HS256")

            login_check = Login(
                employee = Employee.objects.get(employee_code=employee_data.employee_code),
            )
            login_check.save()
           
            return JsonResponse(
                        {
                            "access_token" : encoded_jwt.decode("utf-8"),
                            "name"         : employee_data.name
                         }
                     )
        else:
            return JsonResponse(
                {"message": "INVALID_PASSWORD"},
                status=400
            )
        
