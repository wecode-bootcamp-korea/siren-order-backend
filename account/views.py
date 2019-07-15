import json
import bcrypt
import jwt
import my_settings

from django.shortcuts import render
from account.models   import User, Social, Login
from django.views     import View
from django.http      import JsonResponse


class AccountView(View):
    def post(self, request):
        new_user_info    = json.loads(request.body)

        if User.objects.filter(email = new_user_info['email']).exists():
            return JsonResponse({'message' : '이미 존재하는 이메일입니다.'}, status = 400)

        bytes_pw         = bytes(new_user_info['password'], 'utf-8')
        hashed_pw        = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())

        user_info        = User(
            email        = new_user_info['email'],
            password     = hashed_pw.decode('UTF-8'),
            name         = new_user_info['name'],
            phone_number = new_user_info['phone_number'],
        )
        user_info.save()

        return JsonResponse({'message':'회원가입이 완료되었습니다.'}, status=200)
