from django.urls import path
from .views import *

urlpatterns = [
    path('/sido', CityView.as_view()),
    path('/sido/<int:city_id>', StoreCityView.as_view()),
    path('/gungu/<int:city_id>', GunguView.as_view()),
    path('/shop/<int:gungu_id>', StoreView.as_view()),
]
