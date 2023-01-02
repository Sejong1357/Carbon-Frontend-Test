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

"""
한반도 모듈 파일
Chrome 기준
팔자 주문 조회, 쿠폰(생성, 유효기간 연장, 수동 발급), 카드사 즉시할인(생성, 유효기간 연장) 사용 가능
쿠폰, 카드사 즉시할인의 경우 상품의 할인 기준이 상품번호가 아닌 판매자 기준으로 들어감 
따라서 다음의 판매자가 만든 상품만 쿠폰 및 카드사 즉시할인이 들어가 있음
['qetest01','test4cs2','testtest','TEST4PLAN','test4test','jjang325','hoyeon0808']

쿠폰은 어떤 종류 어떤 값이든 생성 가능하지만 기존의 자동화 쿠폰 사용하기 권장
바이어 쿠폰 1% 100원 2% 200원 3% 300원 4% 400원 5% 500원
['377321', '379319', '377322', '379320', '377323', '379321', '379322', '377324', '379323', '377325']
마케팅 쿠폰 1% 100원 2% 200원 3% 300원 4% 400원 5% 500원
['379324', '379325', '379326', '377326', '377327', '377328', '377329', '377330', '377331','379327']
펀딩 쿠폰 1% 100원 2% 200원 3% 300원 4% 400원 5% 500원
['377332', '379328', '379329', '377333', '377334', '379330', '377335', '379331', '379332', '379333']

카드사 즉시할인 또한 어떤 값이든 생성 가능하지만 기존의 자동화 카즉을 사용하기 권장
['3154639178', '3154639179', '3154639180', '3154639181', '3154639182']

"""
# 바이어 쿠폰
class buyer_coupon:

    """
    han_id = str형
    han_pw = str형
    coupons_id = list형
    gmarket_id = list형
    """

    def __init__(self,han_id,han_pw):

        self.han_id = han_id
        self.han_pw = han_pw

    # 쿠폰 생성 
    def han_coupons_Creation(self,coupons_variaiton,coupons_price,t_list = ['qetest01','test4cs2','testtest','TEST4PLAN','test4test','jjang325','hoyeon0808'],gmarket_id=None,goods_Number=None,choice=1):

        id = self.han_id
        pw = self.han_pw        
        coupon_screenshot = []
        coupons_id = []

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
        desktopWeb.xpathClick('//li[40]//a[1]',runtext)
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

                if int(coupons_price[num]) <= 10:
                    
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

                if '바이어' in str(coupons_variaiton[numnum]):

                    runtext = '쿠폰 필수정보 > 마케팅쿠폰여부 > N 선택'
                    desktopWeb.idClick('registerMassYnN',runtext)

                    runtext = '쿠폰 필수정보 > 펀딩 여부 > N 선택'
                    desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div/div[2]/table/tbody/tr[6]/td[2]/input[2]',runtext)
                
                elif '마케팅' in str(coupons_variaiton[numnum]):

                    runtext = '쿠폰 필수정보 > 마케팅쿠폰여부 > Y 선택'
                    desktopWeb.idClick('registerMassYnY',runtext)


                elif '펀딩' in str(coupons_variaiton[numnum]):

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

                if choice == 0:

                    runtext = '쿠폰 선택옵션 > 상품번호 > 적용 버튼 선택'
                    desktopWeb.idClick('rdo8_Y',runtext)
                    
                    runtext = '쿠폰 선택옵션 > 상품번호 > 선택 버튼 선택'
                    desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[4]/td[1]/button[1]','enter',runtext)
                    time.sleep(2)

                    runtext = '상품 번호 기입'
                    desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',goods_Number,runtext)
                    time.sleep(1)

                    runtext = '추가 버튼 선택'
                    desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
                    time.sleep(1)

                    runtext = '저장 버튼 선택'
                    desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[3]/div/button[3]',runtext)

                else:

                    runtext = '쿠폰 선택옵션 > 판매자 > 선택 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/table/tbody/tr[5]/td/button',runtext)
                    time.sleep(1)
                    
                    # t = open('txt/python_sellers.txt', 'r')
                    # t_list = t.readlines()

                    # for i in range(len(t_list)):
                    #     t_list[i] = t_list[i].strip()
                    #     t_list[i] = t_list[i].strip("'")

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
                time.sleep(1)

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

            coupon_approval('stc1172','PREAPPROVED',int(coupons_id[numnumnum]))
            coupon_approval('stc1172','APPROVED',int(coupons_id[numnumnum]))

            numnumnum = numnumnum + 1
        
        # 쿠폰 수동발급
        # runtext = '전체메뉴 보기 선택'
        # desktopWeb.idClick('showWholeMenuBtn',runtext)
        # time.sleep(2)

        # runtext = '바이어쿠폰 선택'
        # desktopWeb.xpathClick('//*[@id="oneLevelMenu"]/li[41]',runtext)
        # time.sleep(1)

        # runtext = 'G마켓/G9바이어쿠폰 History 선택'
        # desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[2]',runtext)
        # time.sleep(3)

        # runtext = '바이어쿠폰 수동 발급 > 고객 ID > 선택 버튼 선택'
        # desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[1]/button',runtext)
        # time.sleep(1)

        # b = 0
        # c = len(gmarket_id)
        # while b < c:

        #     runtext = '회원검색 > 회원ID 삭제'
        #     desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input','clear',runtext)
        #     time.sleep(1)

        #     runtext = '회원검색 > 회원ID 기입'
        #     desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',gmarket_id[b],runtext)

        #     runtext = '회원검색 > 추가 버튼 선택'
        #     desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
        #     time.sleep(1)

        #     b = b + 1

        # runtext = '회원검색 > 저장 버튼 선택'
        # desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[3]/div/button[2]',runtext)

        # a = 0
        # while a < coupons_variaiton_number * coupons_price_number:

        #     runtext = '바이어쿠폰 수동 발급 > 쿠폰번호 > 쿠폰번호 삭제'
        #     desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/input','clear',runtext)
        #     time.sleep(1)

        #     runtext = '바이어쿠폰 수동 발급 > 쿠폰번호 > 쿠폰번호 기입'
        #     desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/input',coupons_id[a],runtext)

        #     runtext = '수동발급 버튼 선택'
        #     desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/div/div/button[1]',runtext)

        #     runtext = '경고창 제어'
        #     desktopWeb.alerClose(runtext)
        #     time.sleep(10)

        #     runtext = '경고창 제어'
        #     desktopWeb.alerClose(runtext)

        #     a = a + 1

        common.desktopWebClose()
        print('쿠폰생성 끝')

        return coupons_id

    # 쿠폰 유효기간 연장
    def han_coupons_Extension(self,coupons_id):

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
        desktopWeb.xpathClick('//li[40]//a[1]',runtext)
        time.sleep(1)

        runtext = 'G마켓/G9바이어쿠폰 선택'
        desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[1]',runtext)
        time.sleep(3)

        runtext = 'G마켓/G9바이어쿠폰 관리 > 조회조건 > 쿠폰 ID 선택'
        desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]/select',1,'쿠폰ID',runtext)

        coupons_id_number = len(coupons_id)
        n = 0
        while n < coupons_id_number:

            runtext = 'G마켓/G9바이어쿠폰 관리 > 조회조건 > 쿠폰 ID 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]/input','clear',runtext)
            time.sleep(1)

            runtext = 'G마켓/G9바이어쿠폰 관리 > 조회조건 > 쿠폰 ID 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div[1]/div[2]/div/table/tbody/tr[2]/td[2]/input',coupons_id[n],runtext)

            runtext = '쿠폰 조회 버튼 선택'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div/button','enter',runtext)

            runtext = '쿠폰 선택'
            desktopWeb.xpathClick('//*[@id="tab_id_uuid-pane-master"]/div/div/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div',runtext)
            time.sleep(2)

            today = datetime.today().strftime('%Y%m%d')   
            next_month = datetime.today() + timedelta(90)
            next_month = next_month.strftime('%Y%m%d')

            runtext = '쿠폰 필수정보 > 쿠폰유효기간 > 종료일 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[9]/td[2]/div[2]/input','clear',runtext)
            time.sleep(1)

            runtext = '쿠폰 필수정보 > 쿠폰유효기간 > 종료일 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[9]/td[2]/div[2]/input',next_month,runtext)
            time.sleep(1)

            runtext = '쿠폰 필수정보 > 쿠폰유효기간 > 종료일 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/table/tbody/tr[9]/td[2]/div[2]/input','enter',runtext)

            runtext = '수정 버튼 선택'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[1]/div[2]/div/div/button[2]','enter',runtext)
            time.sleep(1)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '예 버튼 선택'
            desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div/div[2]/div/button[2]','enter',runtext)
            time.sleep(1)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            coupon_approval('stc1172','PREAPPROVED',int(coupons_id[n]))
            coupon_approval('stc1172','APPROVED',int(coupons_id[n]))

            runtext = '등록/수정 버튼 선택'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[2]/div[1]/div[2]/div[2]/div/div/button[1]','enter',runtext)
            time.sleep(1)

            runtext = '예 버튼 선택'
            desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div/div[2]/div/button[2]','enter',runtext)
            time.sleep(1)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            n += 1
        
        common.desktopWebClose()
        print('쿠폰 유효기간 연장 끝')

    # 쿠폰 수동 발급
    def han_coupons_Issuance(self,coupons_id,gmarket_id):
        
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
        desktopWeb.xpathClick('//li[40]//a[1]',runtext)
        time.sleep(1)

        runtext = 'G마켓/G9바이어쿠폰 History 선택'
        desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[2]',runtext)
        time.sleep(3)

        runtext = '바이어쿠폰 수동 발급 > 고객 ID > 선택 버튼 선택'
        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td[1]/button',runtext)
        time.sleep(1)

        b = 0 
        gmarket_id_number = len(gmarket_id)
        while b < gmarket_id_number:
            runtext = '회원검색 > 회원ID 삭제'
            desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input','clear',runtext)
            time.sleep(1)

            runtext = '회원검색 > 회원ID 기입'
            desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',str(gmarket_id[b]),runtext)

            runtext = '회원검색 > 추가 버튼 선택'
            desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/div/button',runtext)
            time.sleep(1)

            b += 1

        runtext = '회원검색 > 저장 버튼 선택'
        desktopWeb.xpathClick('/html/body/div[9]/div[2]/div/div/div[3]/div/button[2]',runtext)
        time.sleep(1)
        
        a = 0
        coupons_id_number = len(coupons_id)
        while a < coupons_id_number:

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

            a += 1

        common.desktopWebClose()
        print('쿠폰 수동 발급 끝')

    # 쿠폰 발급 확인
    def han_cupons_check(self,coupons_id,gmarket_id):

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
        desktopWeb.xpathClick('//li[40]//a[1]',runtext)
        time.sleep(1)

        runtext = 'G마켓/G9바이어쿠폰 History 선택'
        desktopWeb.xpathClick('//*[@id="gmarketMenu"]/a[2]',runtext)
        time.sleep(3)

        runtext = '바이어쿠폰 History조회 > 쿠폰정보 > 쿠폰 ID 선택'
        desktopWeb.xpathSelectby('//tbody/tr[1]/td[2]/select[1]',1,'쿠폰ID',runtext)

        runtext = '바이어쿠폰 History조회 > 쿠폰사용여부 > 미사용 선택'
        desktopWeb.xpathSelectby('//*[@id="reactContainer"]/div/div[2]/div/div[1]/div/table/tbody/tr[2]/td[2]/select',1,'미사용',runtext)
        
        coupons_id_number = len(coupons_id)
        a = 0
        while a < coupons_id_number:

            runtext = '바이어쿠폰 History조회 > 쿠폰정보 > 쿠폰 ID 삭제'
            desktopWeb.xpathKey("//input[@title='조회값']",'clear',runtext)
            time.sleep(1)

            runtext = '바이어쿠폰 History조회 > 쿠폰정보 > 쿠폰 ID 기입'
            desktopWeb.xpathKey("//input[@title='조회값']",str(coupons_id[a]),runtext)
            time.sleep(1)

            gmarket_id_number = len(gmarket_id)
            b = 0
            while b < gmarket_id_number:

                runtext = '바이어쿠폰 History조회 > 고객ID > 고객 ID 삭제'
                desktopWeb.xpathKey("//input[@title='고객ID']",'clear',runtext)
                time.sleep(1)

                runtext = '바이어쿠폰 History조회 > 고객ID > 고객 ID 기입'
                desktopWeb.xpathKey("//input[@title='고객ID']",str(gmarket_id[b]),runtext)
                time.sleep(1)

                runtext = '바이어쿠폰 History조회 > 조회 버튼 선택'
                desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div/div[1]/div/div/div/button','enter',runtext)

                runtext = '쿠폰 확인'   
                runtexttext = '쿠폰 확인 완료'
                check = desktopWeb.xpathClickSkip('//*[@id="reactContainer"]/div/div[2]/div/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div/div[1]/div[27]/div/div/span/div/label',runtext,runtexttext)

                b += 1

            a += 1

        common.desktopWebClose()
        print('쿠폰 발급 확인 끝')

        return check

# Item할인/수수료
class Itemdiscount_fee:

    def __init__(self,han_id,han_pw):

        self.han_id = han_id
        self.han_pw = han_pw

    # 팔자 주문 조회
    def palja(self,product):

        han_id = self.han_id
        han_pw = self.han_pw

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

        runtext = '상품번호 삭제'
        desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div/div/table/tbody/tr[1]/td[1]/input[1]','clear',runtext)

        runtext = '상품번호 기입'
        desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div/div/table/tbody/tr[1]/td[1]/input[1]',product,runtext)

        runtext = '조회버튼 선택'
        desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[1]/div/div/div/div[2]/button',runtext)
        time.sleep(2)

        runtext = '경고창 제어'
        error = desktopWeb.alerClose(runtext)
        if error == None:

            runtext = '상품명 추출'
            name = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[3]','value',runtext)

            runtext = '상품값 추출'
            price = desktopWeb.xpathReturnText('//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[8]/div/div/span/div',runtext)
            price = price.replace(',','')

            runtext = '판매자ID 추출'
            sellers = desktopWeb.xpathReturnAttribute('//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]/div/div[2]/div/div/div[2]/div/div/div[2]/div/div[4]','value',runtext)

            runtext = '결과값 스크린 샷'
            desktopWeb.webScreenshot('palja/'+ product,'//*[@id="reactContainer"]/div/div[3]/div/div[3]/div[1]',runtext)
            time.sleep(1)

            runtext = '팔자주문 추가 > 상품번호 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[2]/div[1]/table/tbody/tr/td/input','clear',runtext)

            runtext = '팔자주문 추가 > 상품번호 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[2]/div[1]/table/tbody/tr/td/input',product,runtext)

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
            desktopWeb.webScreenshot('palja/'+ product +'result','//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]',runtext)
            time.sleep(1)

            runtext = '팔자주문 추가버튼 선택'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[3]/div/div[4]/div[3]/div[3]/div/div[1]/button[1]',runtext)
            time.sleep(1)

            runtext = '경고창 제어'
            alret = desktopWeb.alerClose(runtext)
        
        else:
            
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

        common.desktopWebClose()
        print('한반도 끝')

        return name, result, sellers

# 기타 할인
class other_discount:

    def __init__(self,han_id,han_pw):

        self.han_id = han_id
        self.han_pw = han_pw

    # 카드사 즉시할인 생성
    def han_cards(self,cards_price,t_list = ['qetest01','test4cs2','testtest','TEST4PLAN','test4test','jjang325','hoyeon0808']):
        
        id = self.han_id
        pw = self.han_pw    
        card_screenshot = []
        cards_id = []

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

            runtext = '결제수단 설정 > 대분류 선택 추출'
            large = desktopWeb.xpathReturnText('//body[1]/div[9]/div[2]/div[1]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/select[1]',runtext)

            large = large.split('\n')
            n = 0
            a = []
            for i in large:

                if '신용/체크' in i:
                    a.append(n)
                elif '현금결제' in i:
                    a.append(n)
                elif '휴대폰' in i:
                    a.append(n)
                elif '간편결제' in i:
                    a.append(n)
                    
                n += 1

            aa = len(a)
            n = 0
            while n < aa:

                runtext = '결제수단 설정 > 대분류 선택'
                desktopWeb.xpathSelectby('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/select[1]',2,a[n],runtext)
                time.sleep(1)

                runtext = '결제수단 설정 > 중분류 선택 추출'
                middle = desktopWeb.xpathReturnText('//body[1]/div[9]/div[2]/div[1]/div[1]/div[2]/div[1]/table[1]/tbody[1]/tr[1]/td[1]/select[2]',runtext)

                middle = middle.split('\n')
                nn = 0
                b = []
                for i in middle:

                    if '신용/체크' in i:
                        b.append(nn)
                    elif '해외발급' in i:
                        b.append(nn)
                    elif '무통장' in i:
                        b.append(nn)
                    elif '실시간' in i:
                        b.append(nn)
                    elif '은행' in i:
                        b.append(nn)
                    elif '티머니' in i:
                        b.append(nn)
                    elif '휴대폰' in i:
                        b.append(nn)
                    elif '옐로' in i:
                        b.append(nn)
                    elif '체크/신용' in i:
                        b.append(nn)
                    
                    nn += 1
                
                bb = len(b)
                nn = 0
                while nn < bb:

                    runtext = '결제수단 설정 > 중분류 선택'
                    desktopWeb.xpathSelectby('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/select[2]',2,b[nn],runtext)
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

            numnum = 0
            while numnum < len(t_list):

                runtext = '판매자ID 기입'
                desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div[2]/div[1]/table/tbody/tr/td/input',str(t_list[numnum]),runtext)
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

    # 카드사 즉시할인 유효기간 연장
    def han_cards_Extension(self,cards_id):

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
        n = 0
        while n < len(cards_id):

            runtext = '결제수단별 즉시할인 관리 > 정책번호 > 정책번호 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input','clear',runtext)

            runtext = '결제수단별 즉시할인 관리 > 정책번호 > 정책번호 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/table/tbody/tr[1]/td[1]/input',cards_id[n],runtext)

            runtext = '조회 버튼 선택'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/div/div/button','enter',runtext)
            time.sleep(1)

            runtext = '할인 조회'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/span/div',runtext)
            time.sleep(2)

            runtext = '할인발행기간 > 종료일 삭제'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[7]/td[1]/div[2]/input','clear',runtext)
            time.sleep(1)

            today = datetime.today().strftime('%Y%m%d')   
            next_month = datetime.today() + timedelta(90)
            next_month = next_month.strftime('%Y%m%d')

            runtext = '할인발행기간 > 종료일 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[7]/td[1]/div[2]/input',next_month,runtext)
            time.sleep(1)

            runtext = '할인발행기간 > 종료일 기입'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[1]/table/tbody/tr[7]/td[1]/div[2]/input','enter',runtext)
            time.sleep(2)

            runtext = '등록/수정 버튼 선택'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[2]/div[1]/div[3]/div/div/button[1]','enter',runtext)
            time.sleep(1)

            runtext = '예 버튼 선택'
            desktopWeb.xpathKey('/html/body/div[9]/div[2]/div/div/div/div[2]/div/button[2]','enter',runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '경고창 제어'
            desktopWeb.alerClose(runtext)

            card_approval('stc1172','PREAPPROVED',int(cards_id[n]))
            card_approval('stc1172','APPROVED',int(cards_id[n]))

            runtext = '조회 버튼 선택'
            desktopWeb.xpathKey('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[1]/div/div/button','enter',runtext)
            time.sleep(1)

            runtext = '할인 조회'
            desktopWeb.xpathClick('//*[@id="reactContainer"]/div/div[2]/div[1]/div[1]/div[2]/div[2]/div/div/div/div[2]/div/div/div/div/div[1]/div/div/span/div',runtext)
            time.sleep(2)

            n += 1

        common.desktopWebClose()
        print('카드사 즉시할인 연장 끝')



