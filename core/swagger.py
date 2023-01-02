import requests
import json
import datetime
from datetime import datetime, timedelta


def item_discount(a, b, c):

    a = int(a)
    b = int(b)
    c = int(c)
    with open('json/item_discount.json', 'r', encoding='UTF-8') as json_data:
        data = json.load(json_data)

    tomorrow = datetime.today() + timedelta(1)
    tomorrow = tomorrow.strftime('%Y-%m-%d')
    yesterday = datetime.today() - timedelta(1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    tomorrow = str(tomorrow)
    yesterday = str(yesterday)
    if b == 1:
        data['ItemDiscount']['CostUnit'] = "M"
        data['ItemDiscount']['CostPrice'] = c
        data['ItemDiscount']['CostRate'] = 0
    elif b == 2:
        data['ItemDiscount']['CostUnit'] = "R"
        data['ItemDiscount']['CostPrice'] = 0
        data['ItemDiscount']['CostRate'] = c
    data['ItemDiscount']['StartDate'] = yesterday+"T05:54:52.980Z"
    data['ItemDiscount']['EndDate'] = tomorrow+"T05:54:52.980Z"
    data['ItemDiscount']['ItemNo'] = a

    with open('json/item_discount.json', 'w', encoding='UTF-8') as json_data:
        json.dump(data,json_data,indent="\t", ensure_ascii=False)

    with open('json/item_discount.json', 'r', encoding='UTF-8') as json_data:
        data = json.load(json_data)

    params = {
        
        "Content-Type":"application/json"
    }


    Itemdiscount = requests.post('http://discountapi-dev.gmarket.co.kr/SetItemDiscountInfo', json=data,
                        headers=params)

def coupon_approval(id,appstatus,number):

    with open('json/coupon_approval.json', 'r', encoding='UTF-8') as json_data:
        data = json.load(json_data)

    data['AdminId'] = id
    data['ApprStatus'] = appstatus
    data['CouponMasterNoList'] = [number]

    with open('json/coupon_approval.json', 'w', encoding='UTF-8') as json_data:
        json.dump(data,json_data,indent="\t", ensure_ascii=False)

    with open('json/coupon_approval.json', 'r', encoding='UTF-8') as json_data:
        data = json.load(json_data)

    params = {
        
        "Content-Type":"application/json"
    }

    requests.post('http://couponapi-dev.gmarket.co.kr/Admin/Coupon/SetCouponMasterToApprove', json=data,
                        headers=params)

def card_approval(id,appstatus,number):

    with open('json/card_approval.json', 'r', encoding='UTF-8') as json_data:
        data = json.load(json_data)

    data['AdminId'] = id
    data['ApprStatus'] = appstatus
    data['ExtraMasterNoList'] = [number]

    with open('json/card_approval.json', 'w', encoding='UTF-8') as json_data:
        json.dump(data,json_data,indent="\t", ensure_ascii=False)

    with open('json/card_approval.json', 'r', encoding='UTF-8') as json_data:
        data = json.load(json_data)

    params = {
        
        "Content-Type":"application/json"
    }

    requests.post('http://discountapi-dev.gmarket.co.kr/Admin/ExtraDiscount/SetExtraMasterToApprove', json=data,
                        headers=params)