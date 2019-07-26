import json

from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from .models import Cart, Orders, Process, History, ProductType, ProductSize, Options
from account.models import User, Employee
from store.models import Store
from product.models import Product, ProductType, Hot

class CartView(View):

    def product_get(self, product_type, product_id):
        if ProductType.objects.get(id=product_type).name == "HOT":
            return Hot.objects.get(id=product_id)
        else: 
            return Product.objects.get(id=product_id)

    def get(self, request):
        order_list = [{
                      'id'          : order['id'],
                      'product'     : self.product_get(order['product_type_id'],order['product']).name,
                      'amount'      : order['amount'],
                      'price'       : order['price'],
                      'options'     : Options.objects.get(id=order['options_id']).name,
                      'size'        : ProductSize.objects.get(id=order['product_size_id']).name,
                      'type'        : ProductType.objects.get(id=order['product_type_id']).name,
                      'category'    : Product.objects.get(id=order['product']).category_id
                     }for order in Orders.objects.filter(user_id=1).values()]

        return JsonResponse(order_list, safe=False, status=200)

    def post(self, request):
        data = json.loads(request.body)
        order_objs = []
       
        count      = int(data["amount"])
        type_id    = int(data['product_type'])
        product    = self.product_get(data['product_type'],data["product_id"])
        size       = ProductSize.objects.get(id=data['product_size'])
               
        if type_id == 1:
            product_price = product.get_price(size.name)
        elif type_id == 2:
            product_price = Product.objects.get(id=product.product_id).get_price(size.name)
        else:
            product_price = product.price       

        for order_data in range(count):
            order_objs.append(
                Orders(
                    user_id = 1,
                    product = product.id,
                    product_size_id = data['product_size'],
                    options_id = data['options'],
                    amount = int(data['amount'])//int(data['amount']),
                    product_type_id = data['product_type'],
                    price = product_price
                )
            )
        Orders.objects.bulk_create(order_objs) 

        return JsonResponse({'message':'SUCCESS'}, status=200)                  

class CartDelete(View):
    def post(self, request):
        data = json.loads(request.body)
        
        if Orders.objects.filter(id=data['id']).exists():
            Orders.objects.get(id=data['id']).delete()
            return JsonResponse({"message":"SUCCESS"},status=200)
        else:
            return JsonResponse({"message":"INVALID_ID"},status=200)
