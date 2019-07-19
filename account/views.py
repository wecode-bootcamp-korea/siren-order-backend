import json
import bcrypt
import jwt
import my_settings

from account.models   import User, Social, Login
from django.views     import View
from django.http      import JsonResponse
from datetime         import datetime

class AccountView(View):
    def post(self, request):
        new_user_info = json.loads(request.body)

        if User.objects.filter(email = new_user_info['email']).exists():
            return JsonResponse({'message' : 'DUPLICATE_EMAIL'}, status = 400)

        if User.objects.filter(phone_number = new_user_info['phone_number']).exists():
            return JsonResponse({'message' : 'DUPLICATE_PHONE_NUMBER'}, status = 400)

        bytes_pw  = bytes(new_user_info['password'], 'utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())

        user_info = User(
            email        = new_user_info['email'],
            password     = hashed_pw.decode('UTF-8'),
            name         = new_user_info['name'],
            phone_number = new_user_info['phone_number'],
        )
        user_info.save()

        return JsonResponse({'message':'SUCCESS'}, status=200)

class LoginView(View):
    def post(self, request):
        login_user_info = json.loads(request.body)

        try:
            user = User.objects.get(email=login_user_info['email'])
        except User.DoesNotExist:
            return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)
        print(login_user_info['password'])
        if bcrypt.checkpw(login_user_info['password'].encode('UTF-8'), user.password.encode('UTF-8')):
            jwt_token = jwt.encode({'id':user.id}, my_settings.SIREN_SECRET['secret'], algorithm='HS256')

            Login_check = Login(
                user = User.objects.get(email=user.email),
            )
            Login_check.save()

            return JsonResponse({
                'access_token' : jwt_token.decode('UTF-8'),
                'user_name'    : user.name
            }, status = 200)
        else:
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status = 400)
