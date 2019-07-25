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
from account.utils       import login_required

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
                    'user_name'    : user.name,
                    'email'        : user.email
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

class ChangePasswordView(View):
    '''
    유저가 패스워드 변경을 시도하면
    jwt토큰과 유저의 원래 패스워드, 변경하고 싶은 패스워드를 받고
    i)유저의 이메일이 기존에 가입되어 있는 유저인지(데코레이터가 확인),
    ii)유저의 기존 패스워드가 동일한지 체크해서
    맞다면 유저의 패스워드를 변경
    기존 패스워드가 아닐 경우 > INVALID_PASSWORD
    '''
    @login_required
    def post(self, request):
        user_info = json.loads(request.body)
        new_pw = user_info["new_password"]
        current_pw = user_info["current_password"]

        if bcrypt.checkpw(current_pw.encode("UTF-8"), request.user.password.encode("UTF-8")):

            bytes_pw = bytes(new_pw, 'utf-8')
            new_hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())

            request.user.password = new_hashed_pw.decode('UTF-8')
            request.user.save()

            return JsonResponse(
                {
                    "message" : "SUCCESS"
                }, status = 200)

        else:
            return JsonResponse(
                {
                    "message" : "INVALID_PASSWORD"
                }, status = 400)

#class ChangePhoneNumberView(View):
#
#    @login_required
#    def post(self, request):
#        user_info = json.loads(request.body)
#        current_ph = user_info["current_phone_number"]
#        new_ph = user_info["new_phone_number"]
#
#        if bcrypt.checkpw(current_pw.encode("UTF-8"), request.user.password.encode("UTF-8")):
#            request.user.phone_number = current_ph
#            request.user.save()
#
#            return JsonResponse(
#                {
#                    "message" : "SUCCESS"
#                }, status = 400)
#
#        else:
#            return JsonResponse(
#                {
#                    "message" : "INVALID_PASSWORD"
#                }, status = 400)
#
#class EmployeeSocialLoginView(View):
#
#    #@employee_login_required
#    def get(self, request):
#        kakao_token = request.headers["Authorization"]
#        employee_token = reques.headers["
#


