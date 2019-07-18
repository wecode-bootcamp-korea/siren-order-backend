import requests as rq
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sirenorder.settings")
import django
django.setup()
from store.models import City, Gungu, Store

sido = []

url = 'https://www.istarbucks.co.kr/store/getSidoList.do'
res = rq.post(url, data={
    'rndCod' : 'IOM5RNMMAC'
})

dosi_list = res.json()

for dosi in dosi_list['list']:
    print(dosi['sido_cd'])
    sido.append(dosi['sido_cd'])
    print(sido)
   # City.objects.create(name=dosi['sido_nm'],code=dosi['sido_cd'])

gu = {}
def get_gugun(dosi_code):
    url = 'https://www.istarbucks.co.kr/store/getGugunList.do'

    res = rq.post(url, data={
        'sido_cd':dosi_code
    })
  
    gugun_list = res.json()
    gungu = []
    for gugun in gugun_list['list']:
        gungu.append(gugun['gugun_cd'])
        print(gugun['gugun_nm'],gugun['gugun_cd'],dosi_code)
    return gungu
       # Gungu.objects.create(name=gugun['gugun_nm'],code=gugun['gugun_cd'],city_id=dosi_code)

if __name__ == '__main__':
    for i in sido:
        print(i) 
        gu[i]=get_gugun(i)

print(gu)

def get_stores(dosi_code, gugun_code):
    url = 'https://www.istarbucks.co.kr/store/getStore.do?r=EZ95V5O076'
    city_code = City.objects.filter(code=dosi_code).values('id')
    gungu_code = Gungu.objects.filter(code=gugun_code).values('id')
    print(city_code[0]["id"])
    print(gungu_code[0]["id"])
    res = rq.post(url, data={
        'ins_lat'   : '37.4358016',
        'ins_lng'   : '126.8785152',
        'p_sido_cd' : dosi_code,
        'p_gugun_cd': gugun_code,
        'in_biz_cd' : '',
        'set_date'  : '',
    })

    store_list = res.json()

    for store in store_list['list']:
        print(f"{store['addr']},{store['fax']},{store['open_dt']},{store['tel']},{store['lot']},{store['lat']},{store['s_name']}")
        Store.objects.create(name=store['s_name'],address=store['addr'],telephone=store['tel'],fax_number=store['fax'],opened_at=store['open_dt'],lat=store['lat'],lng=store['lot'],city_id=city_code[0]["id"],gungu_id=gungu_code[0]["id"])


if __name__ == '__main__':
    for i in gu:
        for j in gu[i]:
            get_stores(i,j)
          

