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

# PATH List
allpath=os.path.abspath(__file__)
scriptpath=os.path.dirname(allpath)
browserpath=scriptpath+'/webdriver/'
sys.path.append(scriptpath)

# 라이브러리 참조하기
from core.lib import *
from core.config import *
from core.package import *
from core.testrail_api import *
from core.slack import *
from core.gmarket import *
from core.ESM import *
from core.han import *
from core.classification import *

han_Id = '' # 한반도 ID 기입
han_Pw = '' # 한반도 PW 기입
ems_ID = 'test4plan' # ESM ID 기입
esm_PW = 'Newpassw@rd2!'# ESM PW 기입
rail_url = 'http://172.30.2.20/' # Testrail url 기입
rail_id = '' # Testrail ID 기입
rail_pw = '' # Testrail PW 기입
run_templet_id = '3124' # 테스트하고자 하는 run templet id 기입
num = 0 # 몇번째 부터 시작할지 정하는 숫자 ex)0이면 1번째 3이면 3번째 TC부터 수행
coupons_id = ''
gmarket_id = ''
while num < 16: # 테스트하고자 하는 수 16이면 16번째 TC까지 자동 테스트

    run_id = testrailControl.get_runId(rail_url,rail_id,rail_pw,run_templet_id,num)
    run_id = str(run_id)

    goods_Number, goods_Price, goods_buyNumber, goods_deliveryCondition, goods_Delivery, deliveryCondition = testrailControl.get_Preconds_Run(rail_url,rail_id,rail_pw,run_id)
    Member, goods_Name, smileCash, goods_smileCash, goods_discount, discount, coupon, double_discount, goods_buyMethod , option, text, calculation, addtion = testrailControl.get_Title_Run(rail_url,rail_id,rail_pw,run_id)
    
    goods_Number = str(goods_Number)
    goods_smileCash = str(goods_smileCash)
    goods_buyNumber = str(goods_buyNumber)

    a = buyer_coupon(han_Id,han_Pw)
    b = Itemdiscount_fee(han_Id,han_Pw)
    c = other_discount(han_Id,han_Pw)

    esm = ESM_controll(ems_ID,esm_PW)
    vip = VIP(Member,goods_Number,goods_Name,goods_Price,goods_discount,discount,double_discount,coupon,goods_buyMethod,goods_Delivery,goods_buyNumber,option,text,calculation,addtion)
    checkout = Checkout(Member,goods_Name,smileCash,goods_smileCash,goods_Delivery,goods_discount,discount,goods_buyMethod,goods_Number)
    order_complete = Order_Completion(goods_Number,goods_Name,goods_discount)

    if goods_discount == 1 or goods_discount == 2 or goods_discount == 3 or double_discount == 1 or double_discount == 2 or double_discount == 3:

        # 쿠폰을 넣을 id 기입 0,1 일반/클럽 3 간편 5 사업자 4 SFC
        if Member == 0 or Member == 1:
            gmarket_id = ''
        elif Member == 3:
            gmarket_id = ''
        elif Member == 5:
            gmarket_id = 'test4dev'
        elif Member == 4:
            gmarket_id = 'testsfc'

        if goods_discount == 1 or double_discount == 1:
            # 쿠폰 번호는 han.py에 적어둠 원하는 쿠폰번호를 기입
            if double_discount != 0:

                if int(coupon) > 10:
                    coupons_id = ['373323']
                
                else:
                    coupons_id = ['373322']
            
            elif double_discount == 0:

                if int(discount) > 10:
                    coupons_id = ['373323']
                
                else:
                    coupons_id = ['373322']
        
        if goods_discount == 2 or double_discount == 2:

            if double_discount != 0:

                if int(coupon) > 10:
                    coupons_id = ['375323']
                
                else:
                    coupons_id = ['375322']


            elif double_discount == 0:

                if int(discount) > 10:
                    coupons_id = ['375323']
                
                else:
                    coupons_id = ['375322']
        
        if goods_discount == 3 or double_discount == 3:

            if double_discount != 0:

                if int(coupon) > 10:
                    coupons_id = ['375327']
            
                else:
                    coupons_id = ['375326']
            
            elif double_discount == 0:

                if int(discount) > 10:
                    coupons_id = ['375327']
                
                else:
                    coupons_id = ['375326']

        x = a.han_coupons_Issuance(coupons_id,gmarket_id)

    # xxx = 0
    xxx = esm.ESM_modify(goods_Number,goods_Price,goods_deliveryCondition,deliveryCondition,goods_discount,discount,goods_Name)
  
    if xxx == 1:

        testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'ESM에서 존재하지 않는 상품입니다.')
    
    elif xxx == 111:

        testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'ESM에서 정상적으로 수정되지 않은 상품입니다.')

    else:

        check = vip.consolidated_VIP3()

        if check == 11:

            testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경 세팅이 정상 적용되지 않아 자동화테스트 실패, 환경 설정후 다시 시도 해주시길 바랍니다.')


        elif check == 111:

            testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈로 인해 자동화테스트 실패, 잠시 후 다시 시도해주시길 바랍니다.')
        
        else:

            check = checkout.consolidated_Checkout()

            if check == 11:

                testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'카드사 즉시할인이 적용되지 않았습니다. 확인 바랍니다.')

            elif check == 111:

                testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈로 인해 자동화테스트 실패, 잠시 후 다시 시도해주시길 바랍니다.')
            
            else:

                check = order_complete.order_completion()

                if check == 1:

                    id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'주문완료창 진입 실패')
                    testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Fail')

                elif check == 2:

                    id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'주문지연으로 인해 주문실패')
                    testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Delay')

                elif check == 3:

                    id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'주문실패')
                    testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Fail')

                elif check == 11:

                    testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈로 인해 자동화테스트 실패')

                else:

                    id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,1,'주문성공')
                    testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Success')

    num = int(num)

    num += 1