import json
import bcrypt
import jwt
import my_settings

from django.shortcuts import render
from account.models   import User, Social, Login
from django.views     import View
from django.http      import JsonResponse
from datetime         import datetime


class AccountView(View):
    def post(self, request):
        new_user_info = json.loads(request.body)

        if User.objects.filter(email = new_user_info['email']).exists():
            return JsonResponse({'message' : 'JOINED_EMAIL'}, status = 400)

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

# class LoginView(View):
#     def post(self, request):
#         login_user_info = json.loads(request.body)

#         if not User.objects.filter(email=login_user_info['email']).exists:
#             return JsonResponse({'message' : 'UNKNOWN_EMAIL'}, status=400)

#         user = User.objects.get(email=login_user_info['email'])

#         if bcrypt.checkpw(login_user_info['password'].encode('UTF-8'), user.password.encode('UTF-8')):

#             now = datetime.now()
#             str_date = now.strftime('%Y-%m-%d %H:%M:%S')
#             Login_check = Login(
#                 logined_at = datetime.now()
#             jwt_token = jwt.encode({'id':user.id}, my_settings.SIREN_SECRET['secret'], algorithm='HS256')
#             return JsonResponse({


