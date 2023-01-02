# -*- coding: utf-8 -*-

# 스크립트 실행 관련 참조 모듈
import sys
import time
import subprocess
import time
import shutil
import os
import json # import json module
import requests
from requests.auth import HTTPBasicAuth
import pyautogui

allpath = os.path.abspath(__file__)
currentpath = os.path.dirname(allpath)
filepath = os.path.dirname(currentpath)
browserpath=filepath+'/webdriver/'
sys.path.append(filepath)

from core.lib import *
from core.config import *
from core.package import *
from core.testrail_api import *
from core.slack import *
from core.swagger import *


###################################################################################
# Description : Smoke TC 조건 
###################################################################################

class SmokeTCauto:

    def __init__(self,position,run_position,rail_url,rail_id,rail_pw):

        self.position = position
        self.run_position = run_position
        self.rail_url = rail_url
        self.rail_id = rail_id
        self.rail_pw = rail_pw
    
    # 회원 종류
    def members(m_list):

        list_number = len(m_list)
        x = []
        n = 0
        while n < list_number:
            x.append(10)
            n = n + 1
        member = random.choices(m_list, x)
        member = str(member[0])
        return member

    # 할인 종류
    def discounts(discount_number,double_coupons_list,double_discounts_list,discount_list,discount_way,discount_price,coupons_price,cards_price):

        if discount_number == 2:
            
            x_number = len(double_coupons_list)
            y_number = len(double_discounts_list)
            z_number = len(discount_way)
            w_number = len(discount_price)
            r_number = len(coupons_price)
            q_number = len(cards_price)


            x = []
            n = 0 
            while n < x_number:
                x.append(10)
                n = n + 1

            y = []
            n = 0
            while n < y_number:
                y.append(10)
                n = n + 1

            z = []
            n = 0
            while n < z_number:
                z.append(10)
                n = n + 1

            w = []
            n = 0
            while n < w_number:
                w.append(10)
                n = n + 1

            r = []
            n = 0
            while n < r_number:
                r.append(10)
                n = n + 1

            q = []
            n = 0
            while n < q_number:
                q.append(10)
                n = n + 1

            double_coupon = random.choices(double_coupons_list, x)
            double_coupon = str(double_coupon[0])
            double_way = random.choices(discount_way, z)
            double_way = str(double_way[0])
            double_price = random.choices(discount_price, w)
            double_price = int(double_price[0])
            coupon_price = random.choices(coupons_price, r)
            coupon_price = int(coupon_price[0])
            a = double_coupon+double_way%coupon_price
            if '정율' in a:
                a = a + '%'

            double_discount = random.choices(double_discounts_list, y)
            double_discount = str(double_discount[0])
            double_way = random.choices(discount_way, z)
            double_way = str(double_way[0])
            double_price = random.choices(discount_price, w)
            double_price = int(double_price[0])
            card_price = random.choices(cards_price, q)
            card_price = int(card_price[0])
            if 'PCS' in double_discount:
                b = double_discount
            else:
                if '카드사' in double_discount:
                    double_way = '(정율)_%d'
                    b = double_discount+double_way%card_price
                    if '정율' in b:
                        b = b + '%'
                else:
                    b = double_discount+double_way%double_price
                    if '정율' in b:
                        b = b + '%'

            final_discount = a +' + '+ b
        
        elif discount_number == 1:
        
            x_number = len(discount_list)
            y_number = len(discount_way)
            z_number = len(discount_price)
            w_number = len(coupons_price)
            r_number = len(cards_price)

            x = []
            n = 0 
            while n < x_number:
                x.append(10)
                n = n + 1

            y = []
            n = 0
            while n < y_number:
                y.append(10)
                n = n + 1

            z = []
            n = 0
            while n < z_number:
                z.append(10)
                n = n + 1

            w = []
            n = 0
            while n < w_number:
                w.append(10)
                n = n + 1

            r = []
            n = 0
            while n < r_number:
                r.append(10)
                n = n + 1

            dsicount = random.choices(discount_list, x)
            dsicount = str(dsicount[0])
            discount_way = random.choices(discount_way, y)
            discount_way = str(discount_way[0])
            discount_price = random.choices(discount_price, z)
            discount_price = int(discount_price[0])
            coupon_price = random.choices(coupons_price, w)
            coupon_price = int(coupon_price[0])
            card_price = random.choices(cards_price, r)
            card_price = int(card_price[0])
            if 'PCS' in dsicount:
                c = dsicount
            else:
                if '쿠폰' in dsicount:
                    c = dsicount+discount_way%coupon_price
                    if '정율' in c:
                        c = c + '%'
                elif '카드사' in dsicount:
                    discount_way = '(정율)_%d'
                    c = dsicount+discount_way%card_price
                    if '정율' in c:
                        c = c + '%'
                else:
                    c = dsicount+discount_way%discount_price
                    if '정율' in c:
                        c = c + '%'

            final_discount = c
        
        elif discount_number == 0:

            final_discount = '없음'

        return final_discount

    # 결제 방법
    def payments(pays_number,s_payments,n_payments):

        if pays_number == 1:

            x_number = len(s_payments)

            x = []
            n = 0
            while n < x_number:
                x.append(10)
                n = n + 1
            payment = random.choices(s_payments, x)
            payment = str(payment[0])

        elif pays_number == 2:

            x_number = len(n_payments)
            x = []
            n = 0
            while n < x_number:
                x.append(10)
                n = n + 1
            payment = random.choices(n_payments, x)
            payment = str(payment[0])

        return payment

    # 스마일캐시
    def smileCash(smile_number,smilecashs):

        if smile_number == 1:

            x_number = len(smilecashs)

            x = []
            n = 0
            while n < x_number:
                x.append(10)
                n = n + 1
            smilecash = random.choices(smilecashs, x)
            smilecash = int(smilecash[0])
            sc = 'Smile Cash %d00원'%smilecash
        
        elif smile_number == 2:

            sc ='없음'
        
        return sc

    # 배송지
    def destinations(address):

        x_number = len(address)

        x = []
        n = 0
        while n < x_number:
            x.append(10)
            n = n + 1
        destination = random.choices(address, x)
        destination = str(destination[0])

        return destination

    # 배송비
    def deliverys_fee(condition):

        x_number = len(condition)

        x = []
        n = 0
        while n < x_number:
            x.append(10)
            n = n + 1
        delivery_fee = random.choices(condition, x)
        delivery_fee = str(delivery_fee[0])

        return delivery_fee

    # 상품 구매개수
    def purchases_number(purchases_number):

        x_number = len(purchases_number)

        x = []
        n = 0
        while n < x_number:
            x.append(10)
            n = n + 1
        purchase_number = random.choices(purchases_number, x)
        purchase_number = str(purchase_number[0])

        return purchase_number

    # 상품 금액
    def product_price(n):
        
        price = randrange(10,n)
        price = int(price)
        if price > 9:
            a , b = divmod(price,10)
            price = str(a)+','+str(b)

        return price

    # 상세 조건 
    def detail_list(products,member_list,d_n,d_nn,double_coupons_list,double_discounts_list,discount_list,discount_way,discount_price,coupons_price,cards_price,pay,pay_number,s_payments,n_payments,sc,sc_number,smilecashs,address,condition,purchases_numbers):

        member = SmokeTCauto.members(member_list)

        #일반/클럽 회원만 나오는 것 
        randomnumber = randrange(1,3)
        randomnumber = int(randomnumber)

        discount_number = random.choices(d_n, d_nn)
        discount_number = int(discount_number[0])
        if member == '비회원':
            discount_number = 0

        if '당일배송' in products:
            double_coupons_list = ['바이어쿠폰','마케팅쿠폰','펀딩쿠폰'] # 중복할인 쿠폰 list
            double_discounts_list = ['Item할인','카드사 즉시할인'] # 중복할인 list
            discount_list = ['바이어쿠폰','마케팅쿠폰','펀딩쿠폰','Item할인','PCS할인','카드사 즉시할인'] # 단일할인 list
        
        elif '방문수령' in products:
            double_coupons_list = ['바이어쿠폰','마케팅쿠폰','펀딩쿠폰'] # 중복할인 쿠폰 list
            double_discounts_list = ['판매자할인','복수구매할인','Item할인',] # 중복할인 list
            discount_list = ['바이어쿠폰','마케팅쿠폰','펀딩쿠폰','Item할인','PCS할인'] # 단일할인 list
        
        elif 'Biz-on' in products or 'Bizon' in products or 'Biz on' in products:
            double_coupons_list = ['바이어쿠폰','마케팅쿠폰','펀딩쿠폰'] # 중복할인 쿠폰 list
            double_discounts_list = ['복수구매할인'] # 중복할인 list
            discount_list = ['복수구매할인'] # 단일할인 list

        
        discount = SmokeTCauto.discounts(discount_number,double_coupons_list,double_discounts_list,discount_list,discount_way,discount_price,coupons_price,cards_price)

        pays = random.choices(pay, pay_number) 
        pays = int(pays[0])

        if member == '비회원' or member == '간편회원':
            payment = SmokeTCauto.payments(2,s_payments,n_payments)
        elif products == 'E쿠폰 상품(선물하기)' or products == 'E쿠폰 상품(본인인증)' or '스마일페이전용' in products:
            payment = SmokeTCauto.payments(1,s_payments,n_payments)
        else:
            payment = SmokeTCauto.payments(pays,s_payments,n_payments)
        
        if len(sc) == 1 or member == '비회원' or member == '간편회원':
            if int(sc[0]) == 1:
                scs = 1
            elif member == '비회원' or member == '간편회원':
                scs = 2
            else:
                scs = 2
        else:
            scs = random.choices(sc, sc_number)
            scs = int(scs[0])

        smilecash = SmokeTCauto.smileCash(scs,smilecashs)

        delivery = SmokeTCauto.destinations(address)

        delivery_fee = SmokeTCauto.deliverys_fee(condition)

        purchas_number = SmokeTCauto.purchases_number(purchases_numbers)
        purchas_number = int(purchas_number)

        if '복수' in discount:
            multi = randrange(3,5)
            multi = int(multi)
            purchas_number = multi

        return member, randomnumber, discount, payment, smilecash, delivery, delivery_fee, purchas_number

    # TC 작성
    def carbon_smoke_test(self,run_name,repeat,products_list,products_number_list,member_list,d_n,d_nn,double_coupons_list,double_discounts_list,discount_list,discount_way,discount_price,coupons_price,cards_price,pay,pay_number,s_payments,n_payments,sc,sc_number,smilecashs,address,condition,purchases_numbers):

        position = self.position
        run_position = self.run_position
        rail_url = self.rail_url
        rail_id = self.rail_id 
        rail_pw = self.rail_pw

        x = []
        num = 0
        while num < repeat:
            
            products_number = len(products_list)
            products_number_list_number = len(products_number_list)

            n = 0

            while n < products_number:

                products = products_list[n]
                product_number = products_number_list[n]

                if products_number != products_number_list_number:
                    print('상품개수와 상품번호 개수가 동일하지 않습니다 다시 확인해주세요')
                    break
                member, randomnumber, discount, payment, smilecash, delivery, delivery_fee, purchas_number = SmokeTCauto.detail_list(products,member_list,d_n,d_nn,double_coupons_list,double_discounts_list,discount_list,discount_way,discount_price,coupons_price,cards_price,pay,pay_number,s_payments,n_payments,sc,sc_number,smilecashs,address,condition,purchases_numbers)

                price = SmokeTCauto.product_price(100)

                last = '주문완료시 체결현황 확인'
                estimate = '10m'
                ref = 'https://docs.google.com/spreadsheets/d/172GGDfEhzVJgAvnwW8FkX-ap0opQACtQa9t0vqeF6bU/edit#gid=1261413627'

                if products == '성인용품' or products == '최대구매제한-X일당X개' or products == '최대구매제한-구매자1명' or '바우처결제' in products or '사은품/덤' in products:

                    if randomnumber == 1:
                        member = '일반회원'
                    elif randomnumber == 2:
                        member = '클럽회원'

                    if '바우처결제' in products:

                        payment = '일반결제 - 온누리 상품권'
                
                elif products == 'E쿠폰 상품(선물하기)' or products == 'E쿠폰 상품(본인인증)' or '스마일페이전용' in products:

                    if randomnumber == 1:
                        member = '일반회원'
                    elif randomnumber == 2:
                        member = '클럽회원'

                    if 'E쿠폰' in products:
                        delivery_fee = '배송비없음'
                        discount = '없음'
                    else:
                        pass

                elif products == '0원상품' or products == '렌탈상품' or products == '0원상품&렌탈상품' or '환금성' in products or '100원' in products:

                    if randomnumber == 1:
                        member = '일반회원'
                    elif randomnumber == 2:
                        member = '클럽회원'

                    if '0원상품' in products or '렌탈상품' in products:
                        delivery_fee = '배송비없음,상담상품'
                    
                    discount = '없음'

                elif 'SFC몰' in products:

                    member = 'SFC회원'
                    
                elif '사업자 스마일클럽전용 상품(Club biz)' in products or 'Biz-on' in products:

                    member = '사업자회원'

                elif '더빠른배송' in products or '스마일배송' in products:

                    if '새벽배송' in products:
                        member = '클럽회원'
                    elif '24시' in products:
                        if randomnumber == 1:
                            member = '일반회원'
                        elif randomnumber == 2:
                            member = '클럽회원'
                    else:
                        pass

                    randomnumber = randrange(1,3)
                    if randomnumber == 1:
                        delivery_fee = '배송비(무료)'
                    elif randomnumber == 2:
                        delivery_fee = '배송비(유료/선결제)'

                elif '판매자예치금' in products:

                    member = '판매자회원'

                elif '당일배송' in products:

                    delivery_fee = '4만원 조건비 무료'

                elif '부가세면세상품' in products:

                    delivery_fee = '배송비(무료)'

                elif '타이어장착' in products or '방문수령' in products:

                    if '타이어장착' in products:
                        delivery_fee = '타이어 장착점에 타이어가 배송되는 비용'
                    elif '방문수령' in products:
                        delivery_fee = '직접 찾아가서 받기(방문수령)'
                
                if '카드사 즉시할인' in discount:

                    if '캐시충전결제' in payment:

                        payment = '간편결제(SmilePay)-신용/체크카드'
                    
                    else:
                        
                        pass

                if '간편결제' in payment:

                    if randomnumber == 1:
                        member == '일반회원'
                    elif randomnumber == 2:
                        member == '클럽회원'

                if smilecash == '없음':

                    pass

                else:

                    if randomnumber == 1:
                        member == '일반회원'
                    elif randomnumber == 2:
                        member == '클럽회원'

                if member == '일반회원':
                    m_1 = '일반회원'
                    m_2 = '일반회원'
                elif member == '클럽회원':
                    m_1 = '클럽회원'
                    m_2 = '스마일클럽회원'
                elif member == '일반/클럽회원':
                    m_1 = '일반/클럽회원'
                    m_2 = '일반/클럽회원'
                elif member == '간편회원':
                    m_1 = '간편회원'
                    m_2 = '간편회원'
                elif member == '비회원':
                    m_1 = '없음'
                    m_2 = '비회원'
                elif member == 'SFC회원':
                    # m_1 = 'test4dev'
                    m_1 = 'SFC회원'
                    m_2 = 'SFC회원'
                elif member == '사업자회원':
                    # m_1 = 'mp3maste'
                    m_1 = '사업자회원'
                    m_2 = '사업자회원'
                else:
                    if '판매자예치금' in products:
                        m_1 = '판매자회원'
                        m_2 = '판매자회원'


                if discount == '없음':

                    if smilecash == '없음':
                        title = member+' > '+products+' > '+payment+' > '+last
                    else:
                        title = member+' > '+products+' > '+payment+' > '+smilecash+' > '+last

                    if '100원' in products:
                        aa = '상품 가격 : 100원\n'
                    elif '0원' in products:
                        aa = '상품 가격 : 0원\n'
                    else:
                        aa = '상품 가격 : %s00원\n'%price
                    precondition = 'Test 환경 : PC\n'+m_2+' : '+m_1+'(Test계정)\n'+products+'\n'+'상품번호:'+product_number+'\n'+aa+'배송 조건 : '+delivery_fee+'\n'+'배송지: '+delivery+'\n'+'구매 수량 : %d개'%purchas_number
                    step = payment

                elif '판매자' in products:

                    title = products+' > '+last

                    if '무통장' in products:

                        precondition = 'Test 환경 : PC\n'+m_1 +':'+ m_2+'(Test계정)\n판매자 예치금 URL : http://dev.gmarket.co.kr/payment/etcpayment/PopupSmoneyPayment.asp\n상품 가격 : %s00원\n결제수단: 무통장 입금(하나은행 제외)'%price
                        step = '일반결제 - 무통장 입급'
                    
                    elif '판매자 직접 결제' in products:

                        precondition = 'Test 환경 : PC\n'+m_1 +':'+ m_2+'(Test계정)\n판매자 예치금 URL : http://dev.gmarket.co.kr/payment/etcpayment/PopupSmoneyPayment.asp\n상품 가격 : %s000원\n결제수단: 판매자 직접 결제'%price
                        step = '판매자 직접 결제'
                    
                    else:

                        precondition = 'Test 환경 : PC\n'+m_1 +':'+ m_2+'(Test계정)\n판매자 예치금 URL : http://dev.gmarket.co.kr/payment/etcpayment/PopupSmoneyPayment.asp\n상품 가격 : %s00원\n결제수단: '%price+products
                        step = products

                elif  'Smile Card 첫 결제' in products:

                    if smilecash == '없음':
                        title = '클럽회원' + ' > ' + '일반상품' + ' > ' + 'Smile card 첫 결제' + ' > ' + '간편결제(SmilePay)-신용/체크카드(스마일카드 T1)결제'  + last
                    else:
                        title = '클럽회원' + ' > ' + '일반상품' + ' > ' + 'Smile card 첫 결제' + ' > ' + '간편결제(SmilePay)-신용/체크카드(스마일카드 T1)결제' + ' > ' + smilecash + ' > ' + last

                    precondition = 'Test 환경 : PC\n스마일클럽회원 : sejong147 (Test계정)\n'+'일반상품\n'+'상품번호: '+product_number+'\n'+'상품 가격 : %s00원\n'%price+'배송 조건 : '+delivery_fee+'\n'+'배송지: '+delivery+'\n'+'구매 수량 : %d개'%purchas_number
                    step = '간편결제(SmilePay)-신용/체크카드(스마일카드 T1)결제'

                else:

                    if smilecash == '없음':
                        title = member+' > '+products+' > '+discount+' > '+payment+' > '+last
                    else:
                        title = member+' > '+products+' > '+discount+' > '+payment+' > '+smilecash+' > '+last

                    if '100원' in products:
                        aa = '상품 가격 : 100원\n'
                    elif '0원' in products:
                        aa = '상품 가격 : 0원\n'
                    else:
                        aa = '상품 가격 : %s00원\n'%price
                    precondition = 'Test 환경 : PC\n'+m_2+' : '+m_1+'(Test계정)\n'+products+'\n'+'상품번호:'+product_number+'\n'+aa+'배송 조건 : '+delivery_fee+'\n'+'배송지: '+delivery+'\n'+'구매 수량 : %d개'%purchas_number
                    step = payment

                tc_id = testrailControl.post(rail_url,rail_id,rail_pw,position,title,ref,estimate,precondition,3,
                '1.VIP진입',
                '1.할인 및 쿠폰 정상적으로 적용 되어야 함.\n![](index.php?/attachments/get/40414)',
                '1. 주문서 진입\n'+step,
                '1.주문금액이 정상적으로 적용 되어야 함.\n![](index.php?/attachments/get/40416)',
                '1. MY G 페이지 진입\n2. G_ADMIN (정산관리>>거래현황>>체결현황) 진입',
                '1. MY G 페이지의 할인금액, 결제금액과 G_ADMIN의 할인금액, 결제금액 등 동일해야 함\n![](index.php?/attachments/get/22337)\n![](index.php?/attachments/get/22338)')
                x.append(str(tc_id))

                n = n + 1
                print(n)
            
            num = num + 1

        if products_number != products_number_list_number:
            pass
        else: 
            # Run 템플릿 작성
            run_id = testrailControl.post_Runtemplate(rail_url,rail_id,rail_pw,run_position,run_name)
            run_id = str(run_id)
            print('생성한 Run template'+run_id)

            # Run TC 생성
            testrailControl.modify_run(rail_url,rail_id,rail_pw,run_id,x)
            print('Run 기입')

###################################################################################
# Description : 상품 환경체크
###################################################################################

class product_Confirmation:

    def __init__(self,position,run_position,rail_url,rail_id,rail_pw,han_id,han_pw):

        self.position = position
        self.run_position = run_position
        self.rail_url = rail_url
        self.rail_id = rail_id
        self.rail_pw = rail_pw
        self.han_id = han_id
        self.han_pw = han_pw

    def han(self,products_number_list):

        han_id = self.han_id
        han_pw = self.han_pw
        a = []
        b = []
        c = []

        runtext = 'Chrome Browser 구동'
        desktopWeb.browserRun("Chrome",browserpath+'chromedriver',runtext)

        runtext = 'DEV 한반도 접속'
        desktopWeb.webaddressConnect("https://han-dev.ebaykorea.com/",runtext)
        time.sleep(1)

        runtext = 'ID 기입'
        desktopWeb.idKey('u_id',han_id,runtext)

        runtext = 'PW 기입'
        desktopWeb.idKey('u_pw',han_pw,runtext)

        runtext = '로그인 버튼 선택'
        desktopWeb.idClick('do_login',runtext)
        time.sleep(3)

        runtext = '전체메뉴 보기 선택'
        desktopWeb.idClick('showWholeMenuBtn',runtext)
        time.sleep(2)

        runtext = 'Item할인/수수료 선택'
        desktopWeb.xpathClick('//*[@id="oneLevelMenu"]/li[2]',runtext)
        time.sleep(1)

        runtext = 'G마켓 Item할인/수수료 선택'
        desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[1]',runtext)
        time.sleep(3)
        n = 0
        while n < len(products_number_list):

            runtext = '상품번호 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div/div/table/tbody/tr[1]/td[1]/input[1]','clear',runtext)

            runtext = '상품번호 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div/div/table/tbody/tr[1]/td[1]/input[1]',products_number_list[n],runtext)

            runtext = '조회버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div/div/div/div[2]/button',runtext)
            time.sleep(2)

            runtext = '경고창 제어'
            error = desktopWeb.alerClose(runtext)
            if error == None:

                runtext = '상품명 추출'
                name = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]','value',runtext)
                a.append(name)

                runtext = '상품값 추출'
                price = desktopWeb.xpathReturnText('//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[8]/div/div/span/div',runtext)
                price = price.replace(',','')

                runtext = '판매자ID 추출'
                sellers = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[4]','value',runtext)
                b.append(sellers)

                runtext = '결과값 스크린 샷'
                desktopWeb.webScreenshot('palja/'+str(n),'//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]',runtext)
                time.sleep(1)

                runtext = '팔자주문 추가 > 상품번호 삭제'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[2]/div[1]/table/tbody/tr/td/input','clear',runtext)

                runtext = '팔자주문 추가 > 상품번호 기입'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[2]/div[1]/table/tbody/tr/td/input',products_number_list[n],runtext)

                runtext = '팔자주문 추가 > 조회버튼 선택'
                desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[2]/div[2]/button',runtext)
                time.sleep(2)

                runtext = '팔자주문 추가 > 판매가 삭제'
                desktopWeb.xpathClear('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[3]/table/tbody/tr[3]/td[1]/input',runtext)
                time.sleep(1)

                runtext = '팔자주문 추가 > 판매가 기입'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[3]/table/tbody/tr[3]/td[1]/input',price,runtext)
                time.sleep(1)

                runtext = '팔자주문 추가 > 상품수량 삭제'
                desktopWeb.xpathClear('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[3]/table/tbody/tr[4]/td[1]/input',runtext)
                time.sleep(1)

                runtext = '팔자주문 추가 > 상품수량 기입'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[3]/table/tbody/tr[4]/td[1]/input','999',runtext)
                time.sleep(1)

                runtext = '결과값 스크린샷'
                desktopWeb.webScreenshot('palja/'+str(n)+str(n),'//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]',runtext)
                time.sleep(1)

                runtext = '팔자주문 추가버튼 선택'
                desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[3]/div/div[1]/button[1]',runtext)
                time.sleep(1)

                runtext = '경고창 제어'
                alret = desktopWeb.alerClose(runtext)
            
            else:
                
                a.append('실패')
                b.append('없음')
                print('팔자주문 실패')
                result = 1
                
            if '정상적' in alret:

                result = 0
                pass

            elif '열에 대한 값' in alret:

                print('팔자주문 실패')
                result = 1
            
            elif alret == None:

                print('팔자주문 실패')
                result = 1
            
            else:

                print('팔자주문 실패')
                result = 1

            c.append(result)
            print(n)
            n = n + 1 

        common.desktopWebClose()
        print('한반도 끝')

        name = a
        sellers = b
        result = c

        return name, result, sellers

    def product_confirmatonTCauto(self,run_name,products_number_list):

        position = self.position
        run_position = self.run_position
        rail_url = self.rail_url
        rail_id = self.rail_id
        rail_pw = self.rail_pw

        with open('txt/python_sellers.txt','w') as f:
            f.write('')

        column_data = products_number_list
        number = len(column_data)
        print(number)
            

        x = []
        y = []
        z = []
        w = []
        name, result, sellers = product_Confirmation.han(self,products_number_list)
        # TC 생성 및 한반도 테스트 진행
        n = 0
        num = 0
        while n < number:

            print('상품번호: '+column_data[n])

            if column_data[n] == '123465789' or column_data[n] == 123465789 or column_data[n] == '123456789' or column_data[n] == 123456789:

                num = num + 1

            else:

                tc_id = testrailControl.post(rail_url,rail_id,rail_pw,position,'상품번호: '+ column_data[n] + ' 환경체크(한반도 판매상태 체크)',
                'https://docs.google.com/spreadsheets/d/172GGDfEhzVJgAvnwW8FkX-ap0opQACtQa9t0vqeF6bU/edit#gid=1261413627',
                '10m','상품번호: '+ column_data[n],2,
                "1.자동화 상품 상태 확인 (한반도)\nhttps://han-dev.ebaykorea.com/Hanbando/Authentication/Login\nItem할인/수수료 Item할인/수수료 G마켓 Item할인/수수료 > 자동화 상품 조회 여부 확인",'1.한반도 상품 조회 완료','1.한반도 팔자주문 추가','1.팔자주문 추가 확인')
                tc_id = str(tc_id)
                x.append(int(tc_id))
                y.append(result[n])
                w.append(sellers[n])
                img_number1 = testrailControl.post_attachment(rail_url,rail_id,rail_pw,tc_id,'img/palja/'+str(n))
                img_number1 = str(img_number1)
                img_number2 = testrailControl.post_attachment(rail_url,rail_id,rail_pw,tc_id,'img/palja/'+str(n)+str(n))
                img_number2 = str(img_number2)
                img1 = '![](index.php?/attachments/get/'+img_number1+')'
                img2 = '![](index.php?/attachments/get/'+img_number2+')'
                testrailControl.update_Case(rail_url,rail_id,rail_pw,tc_id,{"title":name[n] + ' 상품번호: '+ column_data[n] + ' 환경체크(한반도 판매상태 체크)',
                "custom_steps_separated": [
                        {
                            "content": "1.자동화 상품 상태 확인 (한반도)\nhttps://han-dev.ebaykorea.com/Hanbando/Authentication/Login\nItem할인/수수료 Item할인/수수료 G마켓 Item할인/수수료 > 자동화 상품 조회 여부 확인",
                            "expected": "1.한반도 상품 조회 완료\n"+img1,
                            "additional_info": "",
                            "refs": ""
                        },
                        {
                            "content": "1.한반도 팔자주문 추가",
                            "expected": "1.팔자주문 추가 확인\n"+img2,
                            "additional_info": "",
                            "refs": ""
                        }
                    ]})

            n = n + 1
            print(n)

        number = number - num

        final_sellers = []

        for value in w:
            if value not in final_sellers:
                final_sellers.append(value)
            elif value == '없음':
                pass

        sellers_numbers = len(final_sellers)
        nn = 0
        while nn < sellers_numbers:

            with open('txt/python_sellers.txt','a') as f:
                    f.write(str(final_sellers[nn])+'\n')
            
            nn = nn + 1

        # Run 템플릿 작성
        run_id = testrailControl.post_Runtemplate(rail_url,rail_id,rail_pw,run_position,run_name)
        run_id = str(run_id)
        print('생성한 Run template'+run_id)

        # Run TC 생성
        testrailControl.modify_run(rail_url,rail_id,rail_pw,run_id,x)
        print('Run 기입')

        # Run TC id 추출
        b = 0
        while b < number:

            test_id = testrailControl.get_runId(rail_url,rail_id,rail_pw,run_id,b)
            test_id = str(test_id)
            z.append(test_id)

            b = b + 1

        # Run 테스트 결과값 기입
        c = 0
        while c < number:

            zz = z[c]
            yy = y[c]
            if yy == 0:
                yy = 1
            elif yy == 1:
                yy = 5
            testrailControl.post_runResult(rail_url,rail_id,rail_pw,str(zz),int(yy))

            c = c + 1

        print('끝')

###################################################################################
# Description : 쿠폰, 카드사 즉시할인 생성 
###################################################################################

class han_coupon_card:

    def __init__(self,position,run_position,rail_url,rail_id,rail_pw,han_id,han_pw):

        self.position = position
        self.run_position = run_position
        self.rail_url = rail_url
        self.rail_id = rail_id
        self.rail_pw = rail_pw
        self.han_id = han_id
        self.han_pw = han_pw
        
    def coupons(self,coupons_variaiton,coupons_price,coupons_id,gmarket_id):

        coupon_screenshot = []
        id = self.han_id
        pw = self.han_pw

        runtext = 'Chrome Browser 구동'
        desktopWeb.browserRun("Chrome",browserpath+'chromedriver',runtext)

        runtext = 'DEV 한반도 접속'
        desktopWeb.webaddressConnect("https://han-dev.ebaykorea.com/",runtext)
        time.sleep(1)

        runtext = 'ID 기입'
        desktopWeb.idKey('u_id',id,runtext)

        runtext = 'PW 기입'
        desktopWeb.idKey('u_pw',pw,runtext)

        runtext = '로그인 버튼 선택'
        desktopWeb.idClick('do_login',runtext)
        time.sleep(3)

        runtext = '전체메뉴 보기 선택'
        desktopWeb.idClick('showWholeMenuBtn',runtext)
        time.sleep(2)

        runtext = '바이어쿠폰 선택'
        desktopWeb.xpathClick('//*[@id="oneLevelMenu"]/li[41]',runtext)
        time.sleep(1)

        runtext = 'G마켓/G9바이어쿠폰 선택'
        desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[1]',runtext)
        time.sleep(3)

        coupons_variaiton_number = len(coupons_variaiton)
        numnum = 0
        while numnum < coupons_variaiton_number:
            
            coupons_price_number = len(coupons_price)
            num = 0
            while num < coupons_price_number:

                runtext = '쿠폰 필수정보 > 중복적용타입 > 중복s 선택'
                desktopWeb.idClick('rd_S',runtext)

                if coupons_price[num] <= 10:
                    
                    runtext = '쿠폰 필수정보 > 쿠폰명 > 쿠폰명 기입'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[3]/td/input','autoCoupon-'+coupons_variaiton[numnum]+'_'+str(coupons_price[num])+'%',runtext)

                    runtext = '쿠폰 필수정보 > 할인률/액 > 정율 선택'
                    desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[7]/td[1]/input[1]',runtext)

                    runtext = '쿠폰 필수정보 > 할인률/액 > 최소주문금액 기입'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[8]/td[1]/div/input[1]','100',runtext)

                    runtext = '쿠폰 필수정보 > 할인률/액 > 할인률 기입'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[8]/td[1]/div/input[2]',str(coupons_price[num]),runtext)

                    runtext = '쿠폰 필수정보 > 할인률/액 > 최대할인금액 기입'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[8]/td[1]/div/input[3]','1000',runtext)

                    runtext = '쿠폰 필수정보 > 요청자 > 체크박스 확인'
                    runruntext = '쿠폰 필수정보 > 요청자 > 체크박스 체크'
                    wow = desktopWeb.xpathSelected('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext,runruntext)

                    if wow == 0:

                        runtext = '쿠폰 필수정보 > 요청자 > 체크박스 선택'
                        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext)

                        runtext = '쿠폰 필수정보 > 요청자 > 체크박스 선택'
                        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext)

                    else:

                        runtext = '쿠폰 필수정보 > 요청자 > 체크박스 선택'
                        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext)
                       
                else:

                    runtext = '쿠폰 필수정보 > 쿠폰명 > 쿠폰명 기입'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[3]/td/input','autoCoupon-'+coupons_variaiton[numnum]+'_'+str(coupons_price[num])+'원',runtext)

                    runtext = '쿠폰 필수정보 > 할인률/액 > 정액 선택'
                    desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[7]/td[1]/input[2]',runtext)

                    runtext = '쿠폰 필수정보 > 할인률/액 > 최소주문금액 기입'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[8]/td[1]/div/input[1]','1000',runtext)

                    runtext = '쿠폰 필수정보 > 할인률/액 > 할인액 기입'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[8]/td[1]/div/input[2]',str(coupons_price[num]),runtext)    

                    runtext = '쿠폰 필수정보 > 요청자 > 체크박스 확인'
                    runruntext = '쿠폰 필수정보 > 요청자 > 체크박스 체크'
                    wow = desktopWeb.xpathSelected('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext,runruntext)

                    if wow == 0:

                        runtext = '쿠폰 필수정보 > 요청자 > 체크박스 선택'
                        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext)

                        runtext = '쿠폰 필수정보 > 요청자 > 체크박스 선택'
                        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext)

                    else:
                        runtext = '쿠폰 필수정보 > 요청자 > 체크박스 선택'
                        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[11]/td[1]/input[2]',runtext)
                
                runtext = '쿠폰 필수정보 > 총예산금액 > 총예산금액 기입'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[4]/td[2]/input','1000000',runtext)

                if '바이어' in coupons_variaiton[numnum]:

                    runtext = '쿠폰 필수정보 > 마케팅쿠폰여부 > N 선택'
                    desktopWeb.idClick('registerMassYnN',runtext)

                    runtext = '쿠폰 필수정보 > 펀딩 여부 > N 선택'
                    desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[6]/td[2]/input[2]',runtext)
                
                elif '마케팅' in coupons_variaiton[numnum]:

                    runtext = '쿠폰 필수정보 > 마케팅쿠폰여부 > Y 선택'
                    desktopWeb.idClick('registerMassYnY',runtext)


                elif '펀딩' in coupons_variaiton[numnum]:

                    runtext = '쿠폰 필수정보 > 마케팅쿠폰여부 > N 선택'
                    desktopWeb.idClick('registerMassYnN',runtext)

                    runtext = '쿠폰 필수정보 > 펀딩 여부 > Y 선택'
                    desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[6]/td[2]/input[1]',runtext)
                time.sleep(1)

                runtext = '등록 버튼 선택'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/div/div/button[1]','enter',runtext)
                time.sleep(1)

                runtext = '경고창 제어'
                desktopWeb.alerClose(runtext)
                time.sleep(1)

                runtext = '예 버튼 선택'
                desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div/div[2]/div/button[2]',runtext)

                runtext = '경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '경고창 제어'
                desktopWeb.alerClose(runtext)
                time.sleep(1)

                runtext = '경고창제어'
                desktopWeb.alerClose(runtext)
                time.sleep(1)

                runtext = '스크린샷'
                desktopWeb.webScreenshot('coupon/'+coupons_variaiton[numnum]+'_'+str(coupons_price[num]),'//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[1]/div[2]',runtext)
                coupon_screenshot.append(coupons_variaiton[numnum]+'_'+str(coupons_price[num]))

                runtext = '쿠폰 선택옵션 > 발행본부 > G9 선택'
                desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[1]/select',1,'G9',runtext)

                runtext = '쿠폰 선택옵션 > 대상고객 > 모든 개인 회원 선택'
                desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[1]/select',1,'모든 개인 회원',runtext)

                runtext = '쿠폰 선택옵션 > 판매자 > 선택 버튼 선택'
                desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[5]/td/button',runtext)
                time.sleep(1)
                
                t = open('txt/python_sellers.txt', 'r')
                t_list = t.readlines()

                for i in range(len(t_list)):
                    t_list[i] = t_list[i].strip()
                    t_list[i] = t_list[i].strip("'")

                n = 0
                while n < len(t_list):

                    runtext = '판매자ID 기입'
                    desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',t_list[n],runtext)
                    time.sleep(1)

                    runtext = '추가 버튼 선택'
                    desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
                    time.sleep(1)

                    runtext = '판매자ID 삭제'
                    desktopWeb.xpathClear('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',runtext)
                    time.sleep(1)

                    n = n + 1
                time.sleep(1)

                runtext = '저장 버튼 선택'
                desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[3]/div/button[3]',runtext)

                runtext = '쿠폰 선택옵션 > 스마일클럽 여부 > N 선택'
                desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]/select',1,'N',runtext)

                runtext = '쿠폰 선택옵션 > 발행목적 > 기타 선택'
                desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[2]/td[2]/select',1,'기타',runtext)

                runtext = '등록/수정 버튼 선택'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div/button[1]','enter',runtext)
                time.sleep(1)

                runtext = '예 버튼 선택'
                desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div/div[2]/div/button[2]',runtext)

                runtext = '경고창제어'
                desktopWeb.alerClose(runtext)
                time.sleep(1)

                runtext = '경고창제어'
                desktopWeb.alerClose(runtext)
                time.sleep(1)

                runtext = '쿠폰 필수정보 > 쿠폰 ID 추출'
                coupon_id = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[1]/td[1]/input','value',runtext)

                coupons_id.append(coupon_id)

                runtext = '위로 스크롤'
                desktopWeb.jsScrollo('0',runtext)
                
                runtext = '쿠폰 조회 선택'
                desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div/button',runtext)
                time.sleep(2)

                num = num + 1

            numnum = numnum + 1

        numnumnum = 0
        while numnumnum < coupons_variaiton_number * coupons_price_number:

            coupon_approval('stc1172','PREAPPROVED',coupons_id[numnumnum])
            coupon_approval('stc1172','APPROVED',coupons_id[numnumnum])

            numnumnum = numnumnum + 1
        
        runtext = '전체메뉴 보기 선택'
        desktopWeb.idClick('showWholeMenuBtn',runtext)
        time.sleep(2)

        runtext = '바이어쿠폰 선택'
        desktopWeb.xpathClick('//*[@id="oneLevelMenu"]/li[41]',runtext)
        time.sleep(1)

        runtext = 'G마켓/G9바이어쿠폰 History 선택'
        desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[2]',runtext)
        time.sleep(3)

        runtext = '바이어쿠폰 수동 발급 > 고객 ID > 선택 버튼 선택'
        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[1]/button',runtext)
        time.sleep(1)

        b = 0
        c = len(gmarket_id)
        while b < c:

            runtext = '회원검색 > 회원ID 삭제'
            desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input','clear',runtext)
            time.sleep(1)

            runtext = '회원검색 > 회원ID 기입'
            desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',gmarket_id[b],runtext)

            runtext = '회원검색 > 추가 버튼 선택'
            desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
            time.sleep(1)

            b = b + 1

        runtext = '회원검색 > 저장 버튼 선택'
        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[3]/div/button[2]',runtext)

        a = 0
        while a < coupons_variaiton_number * coupons_price_number:

            runtext = '바이어쿠폰 수동 발급 > 쿠폰번호 > 쿠폰번호 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/input','clear',runtext)
            time.sleep(1)

            runtext = '바이어쿠폰 수동 발급 > 쿠폰번호 > 쿠폰번호 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/input',coupons_id[a],runtext)

            runtext = '수동발급 버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/div/div/button[1]',runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)
            time.sleep(10)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            a = a + 1

        common.desktopWebClose()
        print('쿠폰생성 끝')

        return coupons_id, coupon_screenshot

    def cards(self,cards_price,cards_id):

        card_screenshot = []
        id = self.han_id
        pw = self.han_pw

        runtext = 'Chrome Browser 구동'
        desktopWeb.browserRun("Chrome",browserpath+'chromedriver',runtext)

        runtext = 'DEV 한반도 접속'
        desktopWeb.webaddressConnect("https://han-dev.ebaykorea.com/",runtext)
        time.sleep(1)

        runtext = 'ID 기입'
        desktopWeb.idKey('u_id',id,runtext)

        runtext = 'PW 기입'
        desktopWeb.idKey('u_pw',pw,runtext)

        runtext = '로그인 버튼 선택'
        desktopWeb.idClick('do_login',runtext)
        time.sleep(3)

        runtext = '전체메뉴 보기 선택'
        desktopWeb.idClick('showWholeMenuBtn',runtext)
        time.sleep(2)

        runtext = '기타할인 선택'
        desktopWeb.xpathClick('//*[@id="oneLevelMenu"]/li[4]',runtext)

        runtext = 'G/G9 결제수단별 즉시할인 관리'
        desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[1]',runtext)
        time.sleep(3)

        cards_price_number = len(cards_price)
        num = 0
        while num < cards_price_number:

            runtext = '선택 버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[2]/td[1]/button',runtext)
            a = [100000003,100000004,100000008,100000009]
            aa = len(a)
            n = 0
            while n < aa:

                runtext = '결제수단 설정 > 대분류 선택'
                desktopWeb.xpathSelectby('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/select[1]',0,str(a[n]),runtext)
                time.sleep(1)

                if n == 0:
                    
                    b = [200000009,200000012]
                    bb = len(b)
                    nn = 0
                    while nn < bb:

                        runtext = '결제수단 설정 > 중분류 선택'
                        desktopWeb.xpathSelectby('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/select[2]',0,str(b[nn]),runtext)
                        time.sleep(1)
                                                    
                        runtext = '결제수단 설정 > 조회 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
                        time.sleep(1)

                        runtext = '결제수단 설정 > 체크박스 확인'
                        runtexttext = '체크박스 선택'
                        select_YN = desktopWeb.idSelected('select-all-checkbox',runtext,runtexttext)
                        
                        if select_YN == 0:

                            runtext = '결제수단 설정 > 체크박스 선택'
                            desktopWeb.idClick('select-all-checkbox',runtext)
                            time.sleep(1)
                        
                        else:

                            pass

                        runtext = '결제수단 설정 > 체크박스 선택'
                        desktopWeb.idClick('select-all-checkbox',runtext)

                        runtext = '결제수단 설정 > 선택추가 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[3]/button',runtext)

                        runtext = '경고창 제어'
                        desktopWeb.alerClose(runtext)
                        time.sleep(1)

                        nn = nn + 1

                elif n == 1:

                    b = [200000002,200000006,200000038]
                    bb = len(b)
                    nn = 0
                    while nn < bb:

                        runtext = '결제수단 설정 > 중분류 선택'
                        desktopWeb.xpathSelectby('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/select[2]',0,str(b[nn]),runtext)
                        time.sleep(1)

                        runtext = '결제수단 설정 > 조회 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)

                        runtext = '결제수단 설정 > 체크박스 확인'
                        runtexttext = '체크박스 선택'
                        select_YN = desktopWeb.idSelected('select-all-checkbox',runtext,runtexttext)
                        
                        if select_YN == 0:

                            runtext = '결제수단 설정 > 체크박스 선택'
                            desktopWeb.idClick('select-all-checkbox',runtext)
                            time.sleep(1)
                        
                        else:

                            pass
                            
                        runtext = '결제수단 설정 > 체크박스 선택'
                        desktopWeb.idClick('select-all-checkbox',runtext)

                        runtext = '결제수단 설정 > 선택추가 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[3]/button',runtext)

                        runtext = '경고창 제어'
                        desktopWeb.alerClose(runtext)
                        time.sleep(1)

                        nn = nn + 1

                elif n == 2:

                    b = [200000003,200000004,200000027]
                    bb = len(b)
                    nn = 0
                    while nn < bb:

                        runtext = '결제수단 설정 > 중분류 선택'
                        desktopWeb.xpathSelectby('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/select[2]',0,str(b[nn]),runtext)
                        time.sleep(1)

                        runtext = '결제수단 설정 > 조회 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)

                        runtext = '결제수단 설정 > 체크박스 확인'
                        runtexttext = '체크박스 선택'
                        select_YN = desktopWeb.idSelected('select-all-checkbox',runtext,runtexttext)
                        
                        if select_YN == 0:

                            runtext = '결제수단 설정 > 체크박스 선택'
                            desktopWeb.idClick('select-all-checkbox',runtext)
                            time.sleep(1)
                        
                        else:

                            pass
                            
                        runtext = '결제수단 설정 > 체크박스 선택'
                        desktopWeb.idClick('select-all-checkbox',runtext)

                        runtext = '결제수단 설정 > 선택추가 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[3]/button',runtext)

                        runtext = '경고창 제어'
                        desktopWeb.alerClose(runtext)
                        time.sleep(1)

                        nn = nn + 1

                elif n == 3:

                    b = [200000035,200000036,200000040]
                    bb = len(b)
                    nn = 0
                    while nn < bb:

                        runtext = '결제수단 설정 > 중분류 선택'
                        desktopWeb.xpathSelectby('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/select[2]',0,str(b[nn]),runtext)
                        time.sleep(1)

                        runtext = '결제수단 설정 > 조회 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
                        time.sleep(1)

                        runtext = '결제수단 설정 > 체크박스 확인'
                        runtexttext = '체크박스 선택'
                        select_YN = desktopWeb.idSelected('select-all-checkbox',runtext,runtexttext)
                        
                        if select_YN == 0:

                            runtext = '결제수단 설정 > 체크박스 선택'
                            desktopWeb.idClick('select-all-checkbox',runtext)
                            time.sleep(1)
                        
                        else:

                            pass
                            
                        runtext = '결제수단 설정 > 체크박스 선택'
                        desktopWeb.idClick('select-all-checkbox',runtext)

                        runtext = '결제수단 설정 > 선택추가 버튼 선택'
                        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[3]/button',runtext)

                        runtext = '경고창 제어'
                        desktopWeb.alerClose(runtext)
                        time.sleep(1)
                    
                        nn = nn + 1

                n = n + 1

            runtext = '저장 버튼 선택'
            desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[3]/div/button[2]',runtext)
            time.sleep(1)

            runtext = '정책명 > 기본 > 이름 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[3]/td[1]/input','clear',runtext)
            time.sleep(1)

            runtext = '정책명 > 기본 > 이름 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[3]/td[1]/input','autoCard-'+str(cards_price[num])+'%',runtext)

            runtext = '할인률 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[3]/td[2]/input','clear',runtext)
            time.sleep(1)

            runtext = '할인률 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[3]/td[2]/input',str(cards_price[num]),runtext)
            
            runtext = '최저기준금액 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[4]/td[2]/input','clear',runtext)
            time.sleep(1)

            runtext = '최저기준금액 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[4]/td[2]/input','1000',runtext)

            runtext = '한도금액 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[5]/td[2]/input','clear',runtext)
            time.sleep(1)

            runtext = '한도금액 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[5]/td[2]/input','100000',runtext)

            runtext = '한도기준 > 기간 내 일일 금액한정 선택'
            desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[6]/td[2]/select',1,'기간 내 일일 금액한정',runtext)

            runtext = '총예산사용여부 > Y 선택'
            desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[7]/td[2]/select',1,'Y',runtext)

            runtext = '총예산 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[8]/td[2]/input','clear',runtext)
            time.sleep(1)

            runtext = '총예산 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[8]/td[2]/input','1000000',runtext)

            runtext = '사이트 선택 > 국문 PC 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[2]/td[2]/input[1]',runtext)

            runtext = '사이트 선택 > 국문 모바일 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[2]/td[2]/input[2]',runtext)

            runtext = '다음단계로 버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/button',runtext)

            runtext = ' 예 버튼 선택'
            desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div/div[2]/div/button[2]',runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)
            time.sleep(1)

            runtext = '스크린샷'
            desktopWeb.webScreenshot('card/'+'autoCard-'+str(cards_price[num]),'//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]',runtext)
            card_screenshot.append('autoCard-'+str(cards_price[num]))

            runtext = '적용대상 > 판매자별 선택'
            desktopWeb.idClick('radioTargetSeller',runtext)

            runtext = '적용대상 > 판매자별 > 선택 버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[3]/table/tbody/tr[1]/td/button',runtext)

            t = open('txt/python_sellers.txt', 'r')
            t_list = t.readlines()

            for i in range(len(t_list)):
                t_list[i] = t_list[i].strip()
                t_list[i] = t_list[i].strip("'")

            numnum = 0
            while numnum < len(t_list):

                runtext = '판매자ID 기입'
                desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',t_list[numnum],runtext)
                time.sleep(1)       

                runtext = '추가 버튼 선택'
                desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
                time.sleep(1)

                runtext = '판매자ID 삭제'
                desktopWeb.xpathClear('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',runtext)
                time.sleep(1)

                numnum = numnum + 1
            time.sleep(1)

            runtext = '판매자 검색 > 저장버튼 선택'
            desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[3]/div/button[3]',runtext)

            runtext = '등록/수정 버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div/div/button[1]',runtext)

            runtext = '아래로 스크롤'
            desktopWeb.jsScrollo("100",runtext)

            runtext = '예 버튼 선택'
            desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div/div[2]/div/button[2]',runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)
            time.sleep(1)

            runtext = '카드사 즉시할인 정책번호 추출'
            card_id = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input','value',runtext)

            cards_id.append(card_id)

            numnumnum = 0
            while numnumnum < cards_price_number:

                card_approval('stc1172','PREAPPROVED',int(card_id))
                card_approval('stc1172','APPROVED',int(card_id))

                numnumnum = numnumnum + 1

            runtext = '위로 스크롤'
            desktopWeb.jsScrollo('0',runtext)

            runtext = '결제수단별 즉시할인 관리 > 정책번호 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input',str(card_id),runtext)

            runtext = '조회 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/div/div/button',runtext)
            time.sleep(2)

            runtext = '확인'
            check = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]','value',runtext)
            
            if int(check) != int(card_id):

                runtext = '위로 스크롤'
                desktopWeb.jsScrollo('0',runtext)

                runtext = '결제수단별 즉시할인 관리 > 정책번호 기입'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input',str(card_id),runtext)

                runtext = '조회 선택'
                desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/div/div/button',runtext)
                time.sleep(2)

                runtext = '확인'
                check = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]','value',runtext)

                runtext = '정책번호 선택'
                desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]',runtext)
                time.sleep(1)

            else:

                runtext = '정책번호 선택'
                desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]',runtext)
                time.sleep(1)

            runtext = '아래로 스크롤'
            desktopWeb.jsScrollo('200',runtext)

            runtext = '사용여부변경 버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div/div/button[3]',runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)
            time.sleep(1)

            runtext = '결제수단별 즉시할인 관리 > 정책번호 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input','clear',runtext)
            time.sleep(1)
            
            runtext = '조회 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/div/div/button',runtext)
            time.sleep(2)



            num = num + 1

        

        common.desktopWebClose()
        print('카드사 즉시할인생성 끝')


        return cards_id, card_screenshot
    
    def auto_coupon_card(self,run_name,coupons_price,cards_price,coupons_variaiton,gmarket_id):

        position = self.position
        run_position = self.run_position
        han_id = self.han_id
        han_pw = self.han_pw
        rail_url = self.rail_url
        rail_id = self.rail_id
        rail_pw = self.rail_pw

        # coupons_price = [1,2,3,4] # 쿠폰 할인 금액
        nnn = len(coupons_price)

        ab = []
        nn = 0
        while nn < nnn:

            ab.append(coupons_price[nn])
            ab.append(100*coupons_price[nn])
            nn = nn + 1

        coupons_price = ab
        coupons_id = []
        cards_id = []
        coupons_id, coupon_screenshot = han_coupon_card.coupons(self,coupons_variaiton,coupons_price,coupons_id,gmarket_id)
        print(coupons_id)

        cards_id, card_screenshot = han_coupon_card.cards(self,cards_price,cards_id)
        print(cards_id)

        # coupons_id = ['1','2','3','4','5','6']
        # coupon_screenshot = ['바이어쿠폰_1','바이어쿠폰_100','마케팅쿠폰_1','마케팅쿠폰_100','펀딩쿠폰_1','펀딩쿠폰_100']
        # cards_id = ['11']
        # card_screenshot = ['autoCard-1']

        a = len(coupons_variaiton)
        b = len(coupons_price)
        c = len(cards_price)

        max = a * b + c
        n = 0
        x = 0
        z = 0
        w = []
        coupon_title = []
        card_title = []

        with open('txt/python_coupons.txt','w') as f:
            f.write('')

        while x < a:
            y = 0
            while y < b:

                if coupons_price[y] < 10:

                    unit = '%'
                else:
                    
                    unit = '원'

                coupon_title.append(coupons_variaiton[x]+'_'+str(coupons_price[y])+unit)
                with open('txt/python_coupons.txt','a') as f:
                    f.write(coupons_variaiton[x]+'_'+str(coupons_price[y])+unit+'\n')

                y = y + 1

            x = x + 1
        print(coupon_title)

        while z < c:

            card_title.append('카드사 즉시할인_'+str(cards_price[z])+'%')
            with open('txt/python_coupons.txt','a') as f:
                f.write('카드사 즉시할인_'+str(cards_price[z])+'%'+'\n')
            

            z = z + 1
        print(card_title)
        x = 0
        y = 0
        z = 0
        while n < max:

            if n < a * b:
                tc_coupon_id = testrailControl.post(rail_url,rail_id,rail_pw,position,coupon_title[n],
                        'https://docs.google.com/spreadsheets/d/172GGDfEhzVJgAvnwW8FkX-ap0opQACtQa9t0vqeF6bU/edit#gid=1261413627',
                        '10m',coupons_variaiton[x]+'\n'+'한반도 ID: '+han_id+'\n'+'쿠폰번호: '+coupons_id[n],2,
                        "1.한반도 진입\n2.전체메뉴 > 바이어쿠폰 > G마켓/G9 바이어쿠폰 진입",'1.정상적으로 진입되어야 함','1.'+coupon_title[n]+' 생성','1.쿠폰 정상적으로 생성되어야 함')
                tc_coupon_id = str(tc_coupon_id)
                w.append(int(tc_coupon_id))
                img_number1 = testrailControl.post_attachment(rail_url,rail_id,rail_pw,tc_coupon_id,'img/coupon/'+coupon_screenshot[n])
                img_number1 = str(img_number1)
                img1 = '![](index.php?/attachments/get/'+img_number1+')'

                testrailControl.update_Case(rail_url,rail_id,rail_pw,tc_coupon_id,
                {"custom_steps_separated": [
                        {
                            "content": "1.한반도 진입\n2.전체메뉴 > 바이어쿠폰 > G마켓/G9 바이어쿠폰 진입",
                            "expected": "1.정상적으로 진입되어야 함",
                            "additional_info": "",
                            "refs": ""
                        },
                        {
                            "content": "1."+coupon_title[n]+" 생성",
                            "expected": "1.할인 정상적으로 생성되어야 함\n"+img1,
                            "additional_info": "",
                            "refs": ""
                        }
                    ]})

            else:
                tc_card_id = testrailControl.post(rail_url,rail_id,rail_pw,position,card_title[n-a*b],
                        'https://docs.google.com/spreadsheets/d/172GGDfEhzVJgAvnwW8FkX-ap0opQACtQa9t0vqeF6bU/edit#gid=1261413627',
                        '10m','카드사 즉시할인\n'+'한반도 ID: '+han_id+'\n'+'할인번호: '+cards_id[n-a*b],2,
                        "1.한반도 진입\n2.전체메뉴 > 기타할인 > G마켓/G9 결제수단별 즉시할인 관리 진입",'1.정상적으로 진입되어야 함','1.카드사 즉시 할인생성','1.할인 정상적으로 생성되어야 함')

                tc_card_id = str(tc_card_id)
                w.append(int(tc_card_id))
                img_number2 = testrailControl.post_attachment(rail_url,rail_id,rail_pw,tc_card_id,'img/card/'+card_screenshot[n-a*b])
                img_number2 = str(img_number2)
                img2 = '![](index.php?/attachments/get/'+img_number2+')'

                testrailControl.update_Case(rail_url,rail_id,rail_pw,tc_card_id,
                {"custom_steps_separated": [
                        {
                            "content": "1.한반도 진입\n2.전체메뉴 > 기타할인 > G마켓/G9 결제수단별 즉시할인 관리 진입",
                            "expected": "1.정상적으로 진입되어야 함",
                            "additional_info": "",
                            "refs": ""
                        },
                        {
                            "content": "1.카드사 즉시 할인생성",
                            "expected": "1.할인 정상적으로 생성되어야 함\n"+img2,
                            "additional_info": "",
                            "refs": ""
                        }
                    ]})


            n = n + 1

        # Run 템플릿 작성
        run_id = testrailControl.post_Runtemplate(rail_url,rail_id,rail_pw,run_position,run_name)
        run_id = str(run_id)
        print('생성한 Run template'+run_id)
        testrailControl.modify_run(rail_url,rail_id,rail_pw,run_id,w)

        # Run TC 생성
        d = 0
        e = []
        while d < max:

            test_id = testrailControl.get_runId(rail_url,rail_id,rail_pw,run_id,d)
            test_id = str(test_id)
            e.append(test_id)

            d = d + 1


        coupons_result = []
        i = 0
        while i < a * b:
            ccc = int(coupons_id[i])
            if ccc > 0:
                coupons_result.append(1)

            elif ccc <= 0:
                coupons_result.append(5)

            i = i + 1


        cards_result = []
        i = 0
        while i < max - a * b:
            ccc = int(cards_id[i])
            if ccc > 0:
                cards_result.append(1)

            elif ccc <= 0:
                cards_result.append(5)

            i = i + 1

        # Run 테스트 결과값 기입
        f = 0
        while f < max:

            ff = e[f]
            if f < a * b:
                coupon_r = coupons_result[f]
                testrailControl.post_runResult(rail_url,rail_id,rail_pw,ff,coupon_r)

            else:
                card_r = cards_result[f-a*b]
                testrailControl.post_runResult(rail_url,rail_id,rail_pw,ff,card_r)


            f = f + 1

        print('끝')
            
    