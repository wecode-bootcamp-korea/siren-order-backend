from django.urls import path
from .views import TotalMenuListView, DrinksDetailView, FoodsDetailView, StuffDetailView, CakeDetailView

urlpatterns = [
    path('', TotalMenuListView.as_view()),
    path('/drink/<int:drink_id>', DrinksDetailView.as_view()),
    path('/food/<int:food_id>', FoodsDetailView.as_view()),
    path('/stuff/<int:stuff_id>', StuffDetailView.as_view()),
    path('/cake/<int:cake_id>', CakeDetailView.as_view())
]
