from account.views import AccountView
from django.views import View
from django.urls import path

urlpatterns = [
    path('',AccountView.as_view())
]
