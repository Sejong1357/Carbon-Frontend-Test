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

"""
PC
일반회원 - hoyeon0808
상품 금액: 4500원
일반상품
바이어쿠폰 정액 -100원
복수구매할인 정율 2%
캐시충전결제
유료/선결제

"""

# ESM + G마켓
goods_Price = '4500' # 상품가격
goods_buyNumber = '4' # 구매개수
goods_Number = '1100310534' # 상품 번호

a = '일반회원' # 회원
b = '일반상품' # 상품종류
c = '바이어쿠폰' # 중복쿠폰종류(중복할인 하고 싶지 않을 경우 없음 이라고 기입)
d = 100 # 중복쿠폰 값(정율은 5이하 정액은 100원에서 500원(100원 단위))
e = '복수구매할인' # 할인종류(중복할인으로 쿠폰이 아닌 쿠폰만 할인하고 싶을 경우 원하는 쿠폰 이름 기입)
f = 2 # 할인 값(정율은 10이하 정액은 10초과 쿠폰의 경우 정율은 5이하 정액은 100원에서 500원(100원 단위))
g = 'n' # 스마일 캐쉬 여부 사용하고 싶을 경우 y 아닐 경우 n
h = 0 # 스마일 캐쉬 금액
i = '간편결제-캐시충전결제' # 결제수단
j = '묶음배송비 - 유료/선결제' # 배송비 종류
k = '기본' # 배송지 - 기본, 제주도, 도서 


Member, goods_Name, option, text, calculation, addtion, double_discount, goods_discount, coupon, discount, smileCash ,goods_smileCash, goods_buyMethod, deliveryCondition, goods_deliveryCondition, goods_Delivery, gmarket_id = condition(a,b,c,d,e,f,g,h,i,j,k)
coupons_variaiton = [c]
coupons_price = [d]

han_Id = '' # 한반도 ID 기입
han_Pw = '' # 한반도 PW 기입
ems_ID = 'test4plan' # ESM ID 기입
esm_PW = 'Newpassw@rd2!'# ESM PW 기입
rail_url = 'http://172.30.2.20/' # Testrail url 기입
rail_id = '' # Testrail ID 기입
rail_pw = '' # Testrail PW 기입
run_id = '3104340' # run_id

hanbando = buyer_coupon(han_Id,han_Pw)
esm = ESM_controll(ems_ID,esm_PW)
vip = VIP(Member,goods_Number,goods_Name,goods_Price,goods_discount,discount,double_discount,coupon,goods_buyMethod,goods_Delivery,goods_buyNumber,option,text,calculation,addtion)
checkout = Checkout(Member,goods_Name,smileCash,goods_smileCash,goods_Delivery,goods_discount,discount,goods_buyMethod,goods_Number)
order_complete = Order_Completion(goods_Number,goods_Name,goods_discount)

# step1
# 1. Precondition Setup
# 2 .구매자hoyeon0808에게 상품 1100310534의 바이어 쿠폰 정액100원 할인 쿠폰 지급.
coupons_id = hanbando.han_coupons_Creation(coupons_variaiton,coupons_price)
hanbando.han_coupons_Issuance(coupons_id,gmarket_id)

# step1 - 기대결과
#바이어 쿠폰 정액100원 할인쿠폰 발급 확인.
check = hanbando.han_cupons_check(coupons_id,gmarket_id)

if check == 'n':

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'쿠폰이 정상적으로 발급되지 않아 자동화 테스트 실패, 다시 시도해주세요')
	quit()

# step2
#1.ESM진입
esm.login(goods_Name)
esm.ESM_HOME()

# step2 - 기대결과
# Precondition과 일치하는지 확인
# 상품 조건 Precondition과 일치하는지 확인.
price_check, seller_discount_check, multiple_purchase_check, delivery_Check, existence  = esm.ESM_check2(goods_Number,goods_Price,goods_deliveryCondition,deliveryCondition,goods_discount,discount)
# existence = esm.ESM_modify2(goods_Number,goods_Price,goods_deliveryCondition,deliveryCondition,goods_discount,discount,goods_Name)

if existence == 1:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'존재하지 않는 상품이라 자동화 테스트 실패, 상품 변경 후 다시 시도해주세요.')
	quit()

elif price_check == 1 or seller_discount_check == 1 or multiple_purchase_check == 1 or delivery_Check == 1:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'precondition과 ESM이 맞지 않아 자동화 테스트 실패, ESM 수정후 다시 시도해주세요.')
	quit()
	
# STEP 3
# 로그인한 상태에서 VIP진입 
# 할인 확인
# 쿠폰 적용
check = vip.consolidated_VIP1()

# STEP3 - 기대결과
if check == 1:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(VIP화면오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 6:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'Precondition오류(판매자할인)로 인해 자동화테스트 실패, ESM을 다시 확인해주세요.')
	quit()

elif check == 2:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(로그인 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 7:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'Precondition오류(복수구매할인)로 인해 자동화테스트 실패, ESM을 다시 확인해주세요.')
	quit()

elif check == 3:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(쿠폰창 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 33:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'Precondition오류(조건에 맞는 쿠폰 X)로 인해 자동화테스트 실패, 한반도를 다시 확인해주세요.')
	quit()

elif check == 5:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(주문서 진입 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

# STEP 4
# 1. 구매하기 버튼 클릭하여 주문서 진입
# 2. 결제수단 선택 - 간편결제 -캐시충전 결제
# 3. 구매하기 버튼 선택
check = checkout.consolidated_Checkout()

# STEP 4 - 기대결과
# 1. 상품이 정상적으로 결제되어야 함
if check == 1:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(주소지변경창오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 3:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(카드사 즉시할인 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 33:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'조건에 맞는 카드사할인이 존재하지 않아 자동화테스트 실패, 카드사 즉시할인 다시 확인 바랍니다.')
	quit()

elif check == 2:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(스마일캐시)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 5:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(결제하기)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 6:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(결제수단오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

# STEP 5
# 1. 주문완료 확인
check = order_complete.order_completion()

# STEP 5 -기대결과
# 1. 상품이 정상적으로 구매되어야 함
if check == 1:

	id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'주문완료창 진입 실패')
	testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Fail')
	quit()

elif check == 2:

	id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'주문지연으로 인해 주문실패')
	testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Delay')
	quit()

elif check == 3:

	id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'주문실패')
	testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Fail')
	quit()

elif check == 11:

	testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,5,'환경적인 이슈(주문완료창 진입 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
	quit()

elif check == 0:

	id = testrailControl.post_runResult(rail_url,rail_id,rail_pw,run_id,1,'주문성공')
	testrailControl.post_attachment_result(rail_url,rail_id,rail_pw,id,'img/Gmarket_dev/screenshot/'+goods_Number+'Success')

