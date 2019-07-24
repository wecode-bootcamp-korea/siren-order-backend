from django.urls import path
from .views import TotalMenuListView

urlpatterns = [
    path('', TotalMenuListView.as_view()),
]
