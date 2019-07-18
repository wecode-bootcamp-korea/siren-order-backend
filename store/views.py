import json
from django.http import JsonResponse
from django.views import View
from django.shortcuts import render, get_list_or_404
from .models import City, Gungu, Store


class CityView(View):

    def get(self, request):
        city_list = list(City.objects.values())
        return JsonResponse( city_list, safe=False, status=200) 

class GunguView(View):
    
    def get(self, request, city_id):
        city = City.objects.get(id = city_id)
        gungu_list = list(Gungu.objects.filter(city_id=city.id).values())
        return JsonResponse(gungu_list, safe=False, status=200)
 
class StoreView(View):
  
    def get(self, request, gungu_id):
        gungu = Gungu.objects.get(id = gungu_id).id
        store_list = get_list_or_404(Store.objects.filter(gungu_id=gungu).values())
        return JsonResponse(store_list, safe=False, status=200)

class StoreCityView(View):
   
    def get(self, request, city_id):
        city = City.objects.get(id = city_id).id
        store_list = get_list_or_404(Store.objects.filter(city_id=city).values())
        return JsonResponse(store_list, safe=False, status=200)
