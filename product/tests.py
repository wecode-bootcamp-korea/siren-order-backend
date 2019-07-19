from django.test    import TestCase
from django.test    import Client
from product.views  import TotalMenuListView
from product.models import Categories, Section, Drinks, Hot, Foods, Stuff, Cake

class ProductModelTest(TestCase):

    def setUp(self):
        category1 = Categories.objects.create(id = 1, name = "음료").id
        category2 = Categories.objects.create(id = 2, name = "푸드").id
        category3 = Categories.objects.create(id = 3, name = "상품").id
        Categories.objects.create(id = 4, name = "홀케이크 예약")

        Section.objects.bulk_create(
            [
            Section(id = 1  , name = "콜드브루"   , category_id = category1),
            Section(id = 3  , name = "에스프레소" , category_id = category1),
            Section(id = 12 , name = "베이커리"   , category_id = category2),
            Section(id = 19 , name = "머크/글라스", category_id = category3)
            ]
        )

        Cake.objects.create(
            id           = 1,
            name         = "피칸브라우니",
            english_name = "Pecan Brownie",
            img_url      = "http://image.istarbucks.co.kr/upload/store/skuimg/2019/06/[9300000002173]_20190612150600937.jpg",
            price        = 23900,
            size         = 16,
            weight       = 500,
            description  = "초콜릿 청크를 넣고 고소한 피칸을 듬뿍 올린 진한 브라우니로 품격있는 선물을 준비하세요.",
            condition    = "",
            category_id  = 4
        )

        Drinks.objects.create(
            id           = 1,
            name         = "돌체 콜드 브루",
            english_name = "Dolce Cold Brew",
            img_url      = "http://image.istarbucks.co.kr/upload/store/skuimg/2019/04/[9200000002081]_20190409153909754.jpg",
            only_ice     = 1,
            oz_price     = 0,
            short_price  = 0,
            tall_price   = 5800,
            grande_price = 6300,
            venti_price  = 6800,
            description  = "무더운 여름철, 동남아 휴가지에서 즐기는 커피를 떠오르게 하는 스타벅스 음료의 베스트 x 베스트 조합인 돌체 콜드 브루를 만나보세요!",
            condition    = "콜드 브루 판매 매장에서만 주문 가능한 음료입니다.",
            section_id   = 1
        )
        Drinks.objects.create( # 뜨거운 음료를 선택할 수 있는 음료일 경우를 테스트하기 위해 create
            id           = 12,
            name         = "아이스 스타벅스 돌체 라떼",
            english_name = "Iced Starbucks Dolce Latte",
            img_url      = "http://image.istarbucks.co.kr/upload/store/skuimg/2015/08/[128695]_20150803100201827.jpg",
            only_ice     = 0,
            oz_price     = 0,
            short_price  = 0,
            tall_price   = 5600,
            grande_price = 6100,
            venti_price  = 6600,
            description  = "커피 향과 부드러움의 조화가 아주 멋진 아이스 커피 입니다.",
            condition    = "디카페인 커피 Tab에서 디카페인, 2/1디카페인 스타벅스 돌체 라떼를 주문할 수 있습니다.",
            section_id   = 3
        )

        Hot.objects.create(
            id           = 1,
            name         = "스타벅스 돌체 라떼",
            english_name = "Starbucks Dolce Latte",
            img_url      = "http://image.istarbucks.co.kr/upload/store/skuimg/2015/07/[128692]_20150723020548334.jpg",
            description = "커피 향과 부드러움의 조화가 아주 멋진 커피 입니다.",
            drink_id     = 12
        )

        Foods.objects.create(
            id           = 1,
            name         = "초콜릿 크런치 볼",
            english_name = "Chocolate Crunch Ball",
            img_url      = "http://image.istarbucks.co.kr/upload/store/skuimg/2019/06/[9300000002164]_20190617141656907.jpg",
            price        = 3900,
            description  = "가나슈 초콜릿과 바삭한 식감의 크런치 볼이 함께 있어 달콤한 맛과 씹는 재미를  더해주는 간식용 데니쉬입니다.",
            condition    = "",
            option       = 0,
            section_id   = 12
        )

        Stuff.objects.create(
            id           = 1,
            name         = "아이코닉 사이렌 머그 355",
            english_name = "Iconic siren mug 355",
            img_url      = "http://image.istarbucks.co.kr/upload/store/skuimg/2019/04/[11100513]_20190429144456596.jpg",
            price        = 10000,
            volume       = 355,
            option       = "핫/아이스겸용",
            description  = "스타벅스의 사이렌 로고를 활용한 세라믹 소재 머그",
            condition    = "선물하기(e-Gift Item) 전용 상품 입니다.",
            section_id   = 19
        )

    def test_get_total_menu(self):
        c = Client()

        response = c.get("/product")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    'products': [
                        {
                            'id': 1,
                            'name': '음료',
                            'menu': [
                                {
                                    'id': 1,
                                    'name': '콜드브루',
                                    'drink': [
                                        {
                                            'id': 1,
                                            'name': '돌체 콜드 브루',
                                            'english_name': 'Dolce Cold Brew',
                                            'img_url': 'http://image.istarbucks.co.kr/upload/store/skuimg/2019/04/[9200000002081]_20190409153909754.jpg',
                                            'oz_price': 0,
                                            'short_price': 0,
                                            'tall_price': 5800,
                                            'grande_price': 6300,
                                            'venti_price': 6800
                                        }
                                    ],
                                    'foods': [],
                                    'stuff': []
                                    },
                                    {
                                    'id': 3,
                                    'name': '에스프레소',
                                    'drink': [
                                        {
                                            'id': 12,
                                            'name': '아이스 스타벅스 돌체 라떼',
                                            'english_name': 'Iced Starbucks Dolce Latte',
                                            'img_url': 'http://image.istarbucks.co.kr/upload/store/skuimg/2015/08/[128695]_20150803100201827.jpg',
                                            'oz_price': 0,
                                            'short_price': 0,
                                            'tall_price': 5600,
                                            'grande_price': 6100,
                                            'venti_price': 6600
                                        }
                                    ],
                                    'foods': [],
                                    'stuff': []
                                }
                            ],
                            'cake': []
                            },
                            {
                            'id': 2,
                            'name': '푸드',
                            'menu': [
                                {
                                    'id': 12,
                                    'name': '베이커리',
                                    'drink': [],
                                    'foods': [
                                        {
                                            'id': 1,
                                            'name': '초콜릿 크런치 볼',
                                            'english_name': 'Chocolate Crunch Ball',
                                            'img_url': 'http://image.istarbucks.co.kr/upload/store/skuimg/2019/06/[9300000002164]_20190617141656907.jpg',
                                            'price': 3900
                                        }
                                    ],
                                    'stuff': []
                                }
                            ],
                            'cake': []
                            },
                            {
                            'id': 3,
                            'name': '상품',
                            'menu': [
                                {
                                    'id': 19,
                                    'name': '머크/글라스',
                                    'drink': [],
                                    'foods': [],
                                    'stuff': [
                                        {
                                            'id': 1,
                                            'name': '아이코닉 사이렌 머그 355',
                                            'english_name': 'Iconic siren mug 355',
                                            'img_url': 'http://image.istarbucks.co.kr/upload/store/skuimg/2019/04/[11100513]_20190429144456596.jpg',
                                            'price': 10000
                                        }
                                    ]
                                }
                            ],
                            'cake': []
                            },
                            {
                            'id': 4,
                            'name': '홀케이크 예약',
                            'menu': [],
                            'cake': [
                                {
                                    'id': 1,
                                    'name': '피칸브라우니',
                                    'english_name': 'Pecan Brownie',
                                    'img_url': 'http://image.istarbucks.co.kr/upload/store/skuimg/2019/06/[9300000002173]_20190612150600937.jpg',
                                    'price': 23900
                                }
                            ]
                        }
                    ]
                }
            )

    def test_get_drink_only_ice_detail(self):
        c = Client()

        response = c.get("/product/drink/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {'menu':
                 [
                     {
                         'id': 1,
                         'name': '돌체 콜드 브루',
                         'english_name': 'Dolce Cold Brew',
                         'oz_price': 0, 'short_price': 0,
                         'tall_price': 5800,
                         'grande_price': 6300,
                         'venti_price': 6800,
                         'condition': '콜드 브루 판매 매장에서만 주문 가능한 음료입니다.', 'description': '무더운 여름철, 동남아 휴가지에서 즐기는 커피를 떠오르게 하는 스타벅스 음료의 베스트 x 베스트 조합인 돌체 콜드 브루를 만나보세요!',
                         'hot': None
                     }
                 ]
            }
        )


    def test_get_drink_hot_detail(self):
        c = Client()

        response = c.get("/product/drink/12")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    'menu': [
                        {
                            'id': 12,
                            'name': '아이스 스타벅스 돌체 라떼',
                            'english_name': 'Iced Starbucks Dolce Latte',
                            'oz_price': 0,
                            'short_price': 0,
                            'tall_price': 5600,
                            'grande_price': 6100,
                            'venti_price': 6600,
                            'condition': '디카페인 커피 Tab에서 디카페인, 2/1디카페인 스타벅스 돌체 라떼를 주문할 수 있습니다.',
                            'description': '커피 향과 부드러움의 조화가 아주 멋진 아이스 커피 입니다.',
                            'hot': [
                                {'id': 1,
                                 'name': '스타벅스 돌체 라떼',
                                 'english_name': 'Starbucks Dolce Latte',
                                 'description': '커피 향과 부드러움의 조화가 아주 멋진 커피 입니다.'
                                }
                            ]
                        }
                    ]
                }
        )

    def test_get_drink_detail_error(self):
        c = Client()

        response = c.get("/product/drink/2")
        self.assertEqual(response.status_code, 400)

    def test_get_food_detail(self):
        c = Client()

        response = c.get("/product/food/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    'menu' : [
                        {
                            'id' : 1,
                            'name' : '초콜릿 크런치 볼',
                            'english_name' : 'Chocolate Crunch Ball',
                            'img_url'      : "http://image.istarbucks.co.kr/upload/store/skuimg/2019/06/[9300000002164]_20190617141656907.jpg",
                            'price'        : 3900,
                            'description'  : "가나슈 초콜릿과 바삭한 식감의 크런치 볼이 함께 있어 달콤한 맛과 씹는 재미를  더해주는 간식용 데니쉬입니다.",
                            'condition' : "",
                            'option' : False
                        }
                    ]
                }
        )

    def test_get_food_detail_error(self):
        c = Client()

        response = c.get("/product/food/2")
        self.assertEqual(response.status_code, 400)

    def test_get_stuff_detail(self):
        c = Client()

        response = c.get('/product/stuff/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    'menu' : [
                        {
                            'id'           : 1,
                            'name'         : '아이코닉 사이렌 머그 355',
                            'english_name' : 'Iconic siren mug 355',
                            'img_url'      : 'http://image.istarbucks.co.kr/upload/store/skuimg/2019/04/[11100513]_20190429144456596.jpg',
                            'price'        : 10000,
                            'volume'       : '355',
                            'option'       : '핫/아이스겸용',
                            'description'  : '스타벅스의 사이렌 로고를 활용한 세라믹 소재 머그',
                            'condition'    : '선물하기(e-Gift Item) 전용 상품 입니다.'
                        }
                    ]
                }
        )

    def test_get_stuff_detail_error(self):
        c = Client()

        response = c.get('/product/stuff/2')
        self.assertEqual(response.status_code, 400)

    def test_get_cake_detail(self):
        c = Client()

        response = c.get('/product/cake/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
                {
                    'menu' : [
                        {
                            'id'           : 1,
                            'name'         : '피칸브라우니',
                            'english_name' : 'Pecan Brownie',
                            'img_url'      : 'http://image.istarbucks.co.kr/upload/store/skuimg/2019/06/[9300000002173]_20190612150600937.jpg',
                            'price'        : 23900,
                            'size'         : '16',
                            'weight'       : '500',
                            'description'  : '초콜릿 청크를 넣고 고소한 피칸을 듬뿍 올린 진한 브라우니로 품격있는 선물을 준비하세요.'
                        }
                    ]
                }
        )

    def test_get_cake_detail_error(self):
        c = Client()

        response = c.get("/product/cake/2")
        self.assertEqual(response.status_code, 400)

