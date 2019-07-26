from product.models import Categories,Section, Product
from django.http    import JsonResponse
from django.views   import View

class TotalMenuListView(View):
    def get_drinks(self, section_id):
        section = Section.objects.get(id = section_id)

        drink_list = [
            {
                'id'           : drink['id'],
                'name'         : drink['name'],
                'english_name' : drink['english_name'],
                'img_url'      : drink['img_url'],
                'oz_price'     : drink['oz_price'],
                'short_price'  : drink['short_price'],
                'tall_price'   : drink['tall_price'],
                'grande_price' : drink['grande_price'],
                'venti_price'  : drink['venti_price']
            } for drink in Drinks.objects.values().filter(section = section)
        ]

        return drink_list

    def get_foods(self, section_id):
        section = Section.objects.get(id = section_id)

        food_list = [
            {
                'id'           : food['id'],
                'name'         : food['name'],
                'english_name' : food['english_name'],
                'img_url'      : food['img_url'],
                'price'        : food['price'],
            } for food in Foods.objects.values().filter(section = section)
        ]

        return food_list

    def get_stuffs(self, section_id):
        section = Section.objects.get(id = section_id)

        stuff_list = [
            {
                'id'           : stuff['id'],
                'name'         : stuff['name'],
                'english_name' : stuff['english_name'],
                'img_url'      : stuff['img_url'],
                'price'        : stuff['price'],
            }for stuff in Stuff.objects.values().filter(section = section)
        ]

        return stuff_list

    def get_cake(self, category_id):
        category = Categories.objects.get(id = category_id)

        cake_list = [
            {
                'id'           : cake['id'],
                'name'         : cake['name'],
                'english_name' : cake['english_name'],
                'img_url'      : cake['img_url'],
                'price'        : cake['price']
            }for cake in Cake.objects.values().filter(category = category)
        ]

        return cake_list

    def get_section(self, category_id):
        category = Categories.objects.get(id = category_id)
        section_list = [
            {
                'id'    : section['id'],
                'name'  : section['name'],
                'drink' : self.get_drinks(section['id']),
                'foods' : self.get_foods(section['id']),
                'stuff' : self.get_stuffs(section['id'])
            } for section in Section.objects.values().filter(category = category)
        ]

        return section_list

    def get(self, request):

        category_list = [
            {
                'id'   : category['id'],
                'name' : category['name'],
                'menu' : self.get_section(category['id']),
                'cake' : self.get_cake(category['id'])
            } for category in Categories.objects.values()
        ]

        return JsonResponse({'products': category_list}, status=200)

class DrinksDetailView(View):
    def get_hot_drink(self, drink_id):
        try:
            hot = Hot.objects.get(drink= drink_id)

            hot_list = [
                {
                    'id'           : hot_drink['id'],
                    'name'         : hot_drink['name'],
                    'english_name' : hot_drink['english_name'],
                    'description'  : hot_drink['description']
                } for hot_drink in Hot.objects.filter(drink_id=drink_id).values()
            ]

            return hot_list

        except Hot.DoesNotExist:
            return None

    def get(self, request, drink_id):
        if Drinks.objects.filter(id=drink_id).exists():
            drink_detail = [
                {
                    'id'           : drink['id'],
                    'name'         : drink['name'],
                    'english_name' : drink['english_name'],
                    'oz_price'     : drink['oz_price'],
                    'short_price'  : drink['short_price'],
                    'tall_price'   : drink['tall_price'],
                    'grande_price' : drink['grande_price'],
                    'venti_price'  : drink['venti_price'],
                    'condition'    : drink['condition'],
                    'description'  : drink['description'],
                    'hot' : self.get_hot_drink(drink['id'])
                } for drink in Drinks.objects.filter(id=drink_id).values()
            ]

            return JsonResponse({'menu' : drink_detail}, status = 200)
        else:
            return HttpResponse(status = 400)

class FoodsDetailView(View):
    def get(self, request, food_id):
        try:
            food = Foods.objects.get(id=food_id)

            food_detail = [
                {
                    'id'           : food.id,
                    'name'         : food.name,
                    'english_name' : food.english_name,
                    'img_url'      : food.img_url,
                    'price'        : food.price,
                    'description'  : food.description,
                    'condition'    : food.condition,
                    'option'       : food.option #옵션이 1일 때 워밍옵션이 있고, 데울지 안데울 지 선택 
                }
            ]

            return JsonResponse({'menu' : food_detail}, status = 200)
        except Foods.DoesNotExist:
            return HttpResponse(status = 400)

class StuffDetailView(View):
    def get(self, request, stuff_id):
        try:
            stuff = Stuff.objects.get(id=stuff_id)

            stuff_detail = [
                {
                    'id'           : stuff.id,
                    'name'         : stuff.name,
                    'english_name' : stuff.english_name,
                    'img_url'      : stuff.img_url,
                    'price'        : stuff.price,
                    'volume'       : stuff.volume,
                    'option'       : stuff.option, # 핫/아이스겸용, 아이스전용 
                    'description'  : stuff.description,
                    'condition'    : stuff.condition
                }
            ]

            return JsonResponse({'menu' : stuff_detail}, status = 200)
        except Stuff.DoesNotExist:
            return HttpResponse(status = 400)

class CakeDetailView(View):
    def get(self, request, cake_id):
        try:
            cake = Cake.objects.get(id=cake_id)

            cake_detail = [
                {
                    'id'           : cake.id,
                    'name'         : cake.name,
                    'english_name' : cake.english_name,
                    'img_url'      : cake.img_url,
                    'price'        : cake.price,
                    'size'         : cake.size,
                    'weight'       : cake.weight,
                    'description'  : cake.description
                }
            ]

            return JsonResponse({'menu' :cake_detail}, status = 200)

        except Cake.DoesNotExist:
            return HttpResponse(status = 400)

