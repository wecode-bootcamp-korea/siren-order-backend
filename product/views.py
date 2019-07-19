from product.models import Categories,Section, Drinks, Foods, Stuff, Hot, Cake
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
                'id'   : section['id'],
                'name' : section['name'],
                'drink':  self.get_drinks(section['id']),
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

