from account.views import *
from django.urls import path

urlpatterns = [
    path('',AccountView.as_view()),
    path('/login', LoginView.as_view()),
    path('/login/chpw', ChangePasswordView.as_view()),
    path('/employee', EmployeeSignup.as_view()),
    path('/employee/login', EmployeeLogin.as_view()),
    path('/employee/kakao', EmployeeSocialLoginView.as_view())
]
