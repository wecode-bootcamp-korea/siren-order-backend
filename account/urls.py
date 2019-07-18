from account.views import AccountView, LoginView
from django.views import View
from django.urls import path

urlpatterns = [
    path('',AccountView.as_view()),
    path('/login', LoginView.as_view())
]
