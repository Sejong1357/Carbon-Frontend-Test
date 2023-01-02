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
filepath = os.path.dirname(allpath)
scriptpath=os.path.dirname(filepath)
browserpath=scriptpath+'/webdriver/'
Gmarket_path = scriptpath + '/img/Gmarket_dev/'
smilepay_path = scriptpath + '\\img\\Gmarket_dev\\smilepay\\'
kbcard_path = scriptpath + '/img/Gmarket_dev/KBcard/'
Chromesetting_path = scriptpath + '/img/Gmarket_dev/Chromesetting/'
# kbcard_path =  scriptpath + '/file/autouipath/kbcard.xaml'
sys.path.append(scriptpath)

# 라이브러리 참조하기
from core.lib import *
from core.config import *
from core.package import *
from core.testrail_api import *
from core.slack import *
import core.swagger

"""
Gmarket 모듈 파일
Chrome 기준
각각의 페이지별로 분류하였지만 독립적으로 사용 불가능(VIP 예외)
순서를 지켜서 사용할것 !!(VIP > Checkout > Order_Completion)
ex) Checkout만 사용하고 싶을시 VIP > Checkout로 사용 가능 / Checkout만 사용 불가능
각 class내에 독립적인 모듈 존재 ex) VIP - coupon만 제어하는 coupons 모듈 존재
각 모듈을 독립적으로 사용할 수 있지만 권장하지 않음
각 class별로 통합본 함수를 만들었으니 사용 권장

"""

class VIP():

    def __init__(self,Member,goods_Number,goods_Name,goods_Price,goods_discount,discount,double_discount,coupon,goods_buyMethod,goods_Delivery,goods_buyNumber,option,text,calculation,addtion):

        self.Member = Member
        self.goods_Number = goods_Number
        self.goods_Name = goods_Name
        self.goods_discount = goods_discount
        self.discount = discount
        self.double_discount = double_discount
        self.coupon = coupon
        self.goods_buyMethod = goods_buyMethod
        self.goods_Delivery = goods_Delivery
        self.goods_buyNumber = goods_buyNumber
        self.goods_Price = goods_Price
        self.option = option
        self.text = text
        self.calculation = calculation
        self.addtion = addtion

    # Item할인
    def itemdiscount(self):

        goods_Number = self.goods_Number
        goods_discount = self.goods_discount
        discount = self.discount

        core.swagger.item_discount(goods_Number,2,0)

        #item 할인
        if goods_discount == 6:

            if discount > 10:
                random = 1
            else:
                random = 2
            random_number = discount
            core.swagger.item_discount(goods_Number,random,random_number)
    
    # VIP 이동
    def VIP_move(self):

        Member = self.Member
        goods_discount = self.goods_discount
        goods_Number = self.goods_Number
        VIP_num = 0

        while VIP_num < 2:

            runtext ='Chrome Browser 구동'
            desktopWeb.browserRun("Chrome",browserpath+'chromedriver',runtext)

            try:
                #SFC회원
                if Member == 4:

                    runtext = 'Chrome 설정창 접속'
                    desktopWeb.webaddressConnect("chrome://settings/clearBrowserData",runtext)

                    runtext = 'Gmarket 상품 VIP 접속'
                    webaddress = "'"+'http://item-dev.gmarket.co.kr/detailview/item.asp?goodscode='+goods_Number+'&GoodsSale=Y&jaehuid=200007272'+"'"
                    desktopWeb.webaddressConnect("chrome://settings/clearBrowserData",runtext)
                    desktopWeb.webaddressadditionalConnect(webaddress,runtext)

                    runtext = '제어창 변경'
                    desktopWeb.popupControl(1,runtext)
                
                #PCS 할인
                elif goods_discount == 8:

                    runtext = 'Chrome 설정창 접속'
                    desktopWeb.webaddressConnect("chrome://settings/clearBrowserData",runtext)

                    runtext = 'Gmarket 상품 VIP 접속'
                    webaddress = "'"+'http://item-dev.gmarket.co.kr/detailview/item.asp?goodscode='+goods_Number+'&GoodsSale=Y&jaehuid=200002617'+"'"
                    desktopWeb.webaddressadditionalConnect(webaddress,runtext)

                    runtext = '제어창 변경'
                    desktopWeb.popupControl(1,runtext)

                #판매자회원
                elif Member == 6:

                    runtext = 'Gmarket 상품 VIP 접속'
                    desktopWeb.webaddressConnect("https://signinssl-dev.gmarket.co.kr/login/login?url=https://www-dev.gmarket.co.kr/",runtext)

                else:
                    
                    runtext = 'Gmarket 상품 VIP 접속'
                    webaddress = 'http://item-dev.gmarket.co.kr/detailview/item.asp?goodscode='+ goods_Number
                    desktopWeb.webaddressConnect(webaddress,runtext)

                VIP_error = 0
                VIP_num += 5

            except:

                VIP_error = 1
                if VIP_num == 0:

                    print('오류로 인해 VIP 화면 진입 불가능')
                    print('진입 재시도')
                    time.sleep(3)
                
                elif VIP_num != 0: 

                    print('VIP 화면 진입 불가능')
                    print('자동화 종료')
                    common.desktopWebClose()

            VIP_num += 1

        time.sleep(2)

        return VIP_error
    
    # 로그인
    def login_process(self):

        Member = self.Member
        goods_Name = self.goods_Name
        VIP_num = 0
        # 일반/클럽/간편 회원 기입할 것

        while VIP_num < 2:
            try:

                #일반+클럽+판매자/간편/비회원/사업자/SFC
                #일반+클럽+사업자
                if Member == 0 or Member == 1 or Member == 6:

                    # 성인용품
                    if goods_Name == 12:

                        pass

                    else:

                        runtext = '로그인 버튼 클릭'
                        desktopWeb.linkTextClick('로그인',runtext)
                    time.sleep(2)

                    runtext = 'ID 입력(일반/클럽/판매자)'
                    desktopWeb.idKey('id','',runtext)

                    runtext = 'PW 입력(일반/클럽/판매자)'
                    desktopWeb.idKey('pwd','',runtext)

                    runtext = '로그인 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="mem_login"]/div[1]/div[3]/button',runtext)

                # 간편회원
                elif Member == 3:

                    runtext = '로그인 버튼 클릭'
                    desktopWeb.linkTextClick('로그인',runtext)

                    runtext = 'ID 입력(간편)'
                    desktopWeb.idKey('id','',runtext)

                    runtext = 'PW 입력(간편)'
                    desktopWeb.idKey('pwd','',runtext)

                    runtext = '로그인 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="mem_login"]/div[1]/div[3]/button',runtext)
                
                # 비회원
                elif Member == 2:

                    pass
                
                # 사업자
                elif Member == 5:

                    runtext = '로그인 버튼 클릭'
                    desktopWeb.linkTextClick('로그인',runtext)

                    runtext = 'ID 입력(사업자)'
                    desktopWeb.idKey('id','test4dev',runtext)

                    runtext = 'PW 입력(사업자)'
                    desktopWeb.idKey('pwd','test1004',runtext)

                    runtext = '로그인 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="mem_login"]/div[1]/div[3]/button',runtext)

                # SFC 회원
                elif Member == 4:

                    runtext = '로그인 버튼 클릭'
                    desktopWeb.linkTextClick('로그인',runtext)

                    runtext = 'ID 입력(SFC)'
                    desktopWeb.idKey('id','testsfc',runtext)

                    runtext = 'PW 입력(SFC)'
                    desktopWeb.idKey('pwd','test1004',runtext)

                    runtext = '로그인 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="mem_login"]/div[1]/div[3]/button',runtext)
                
                time.sleep(5)

                runtext = '로그인 확인'
                loging_button = desktopWeb.xpathCheck('//*[@id="mem_login"]/div[1]/div[3]/button',runtext)

                if loging_button == 'n':

                    VIP_error = 2
                
                else:

                    runtext = '비밀번호 변경 안내'
                    runtexttext = '비밀번호 변경 안내 > 3개월 후 다시 안내 선택'
                    desktopWeb.xpathClickSkip('//*[@id="PasswordChangeInform"]/div/div/div[2]/a[1]',runtext,runtexttext)

                    VIP_error = 0
                    VIP_num += 5
            
            except:
                
                VIP_error = 2
                if VIP_num == 0:

                    print('로그인 오류로 인해 재시도')
                    runtext = '페이지 새로고침'
                    desktopWeb.webrefresh(runtext)
                    time.sleep(3)
                
                elif VIP_num != 0:

                    print('로그인 오류로 인해 진행 불가능')
                    print('자동화 종료')
                    common.desktopWebClose()

            VIP_num += 1
            
        time.sleep(5)

        return VIP_error

    # 상품
    def merchandise(self):

        goods_Name = self.goods_Name
        goods_Delivery = self.goods_Delivery
        option = self.option
        text = self.text
        calculation = self.calculation
        addtion = self.addtion

        # 타이어상품
        if goods_Name == 6:

            runtext = '장착점 선택 버튼 선택'
            desktopWeb.xpathKey('//*[@id="mount_search_info"]/div/button','enter',runtext)

            # 기본(=서울), 도서산간
            if goods_Delivery == 1 or goods_Delivery == 3:

                runtext = '서울 기입'
                desktopWeb.idKey('inputMountSearch','서울',runtext)
                time.sleep(1)

                runtext = '찾기 버튼 선택'
                desktopWeb.xpathClick('//*[@id="mountSearchForm"]/fieldset/p[2]/button[1]',runtext)
                time.sleep(1)

                runtext = '상도점 선택'
                desktopWeb.xpathClick('//*[@id="mount_branch_list"]/li[1]/div[2]/a[1]',runtext)
                time.sleep(1)

            # 제주도
            elif goods_Delivery == 2:

                runtext = '제주 기입'
                desktopWeb.idKey('inputMountSearch','서울',runtext)
                time.sleep(1)

                runtext = '찾기 버튼 선택'
                desktopWeb.xpathClick('//*[@id="mountSearchForm"]/fieldset/p[2]/button[1]',runtext)
                time.sleep(1)

                runtext = '상도점 선택'
                desktopWeb.xpathClick('//*[@id="mount_branch_list"]/li/div[2]/a[1]',runtext)
                time.sleep(1)

        # 방문수령
        elif goods_Name == 8:

            runtext = '배송방법 선택'
            desktopWeb.xpathKey('//*[@id="coreDelivery"]/button','enter',runtext)
            time.sleep(2)

            runtext = '직접 찾아가서 받기 선택'
            desktopWeb.xpathClick('//*[@id="coreDelivery"]/ul/li[2]/a',runtext)

        # 스마일프레시
        elif goods_Name == 27:

            runtext = '배송지 변경 버튼 선택'
            desktopWeb.xpathKey('//*[@id="container"]/div[3]/div[2]/div[2]/ul/li[1]/div[2]/div/div[1]/button','enter',runtext)
            time.sleep(2)

            runtext = '배송지 팝업창 제어'
            desktopWeb.popupControl(1,runtext)

            runtext = 'Frame 변경'
            desktopWeb.frameSwitch(runtext)

            runtext = '배송지 팝업창 오류 확인'
            check = desktopWeb.xpathCheck('//*[@id="ulAddressList"]/li[1]/div[1]/div[1]/span[2]',runtext)

            if check == 'p':

                runtext = '새로고침'
                desktopWeb.webrefresh(runtext)
                time.sleep(3)

            runtext = '배송지 List 확인'
            yy = desktopWeb.idclassnameElement('ulAddressList','list-item',runtext)
            
            n = 1
            while n < yy + 1:
                
                runtext = '배송지 이름 추출'
                zz = desktopWeb.xpathText('//*[@id="ulAddressList"]/li['+str(n)+']/div[1]/div[1]/span[2]',runtext)

                if goods_Delivery == 1:

                    if '서울' in zz:

                        break
                
                elif goods_Delivery == 2:

                    if '제주' in zz:

                        break

                elif goods_Delivery == 3:

                    if '도서' in zz:

                        break
                
                n += 1
            
            runtext = '배송지 고유 id값 추출'
            ww = desktopWeb.xpathReturnAttribute('//*[@id="ulAddressList"]/li['+str(n)+']/div/div[5]/input','id',runtext)

            if ww != '없음':

                runtext = '배송지 선택 버튼 선택'
                desktopWeb.xpathClick('//*[@id="'+str(ww)+'"]/button[2]',runtext)
            
            else:

                runtext = '배송지 변경 > 배송지 추가하기 버튼 선택'
                desktopWeb.xpathKey('//*[@id="content"]/div/button','enter',runtext)
                time.sleep(1)

                runtext = '배송지 추가하기 > 배송지명 삭제'
                desktopWeb.idKey('deliveryName','clear',runtext)
                time.sleep(1)

                if goods_Delivery == 1:

                    runtext = '배송지 추가하기 > 배송지명 기입'
                    desktopWeb.idKey('deliveryName','auto-A권역',runtext)
                
                elif goods_Delivery == 2:

                    runtext = '배송지 추가하기 > 배송지명 기입'
                    desktopWeb.idKey('deliveryName','auto-B권역',runtext)
                
                elif goods_Delivery == 3:

                    runtext = '배송지 추가하기 > 배송지명 기입'
                    desktopWeb.idKey('deliveryName','auto-C권역',runtext)
                time.sleep(1)

                runtext = '배송지 추가하기 > 받는 분 이름 기입'
                desktopWeb.idKey('reciverName','아무나',runtext)
                time.sleep(1)

                runtext = '배송지 추가하기 > 받는 분 연락처 기입'
                desktopWeb.idKey('hpNo','01012345678',runtext)
                time.sleep(1)

                runtext = '배송지 추가하기 > 주소 선택'
                desktopWeb.xpathClick('//*[@id="beforeSearch"]/div/div/button',runtext)
                time.sleep(1)

                runtext = 'Frame 변경'
                desktopWeb.frameSwitch(runtext)
                
                if goods_Delivery == 1:

                    runtext = '주소찾기 > 주소 입력'
                    desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]','강남파이낸스센터',runtext)
                    time.sleep(1)
                
                elif goods_Delivery == 2:

                    runtext = '주소찾기 > 주소 입력'
                    desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]','제주도',runtext)
                    time.sleep(1)
                
                elif goods_Delivery == 3:

                    runtext = '주소찾기 > 주소 입력'
                    desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]','울릉도',runtext)
                    time.sleep(1)
                
                runtext = '주소찾기 > 돋보기 선택'
                desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/button[2]','enter',runtext)
                
                runtext = '주소 찾기 > 주소 선택'
                desktopWeb.xpathClick('//*[@id="1_0"]/a[1]',runtext)
                
                runtext = '이 위치로 배송지 설정 선택'
                desktopWeb.jsClick('//*[@id="container"]/div/div/div[1]/div[4]/div[2]/a',runtext)
                time.sleep(2)

                runtext = '기존 Frame 변경'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'Frame 변경'
                desktopWeb.frameSwitch(runtext)

                runtext = '배송지 추가하기 > 상세주소 기입'
                desktopWeb.idKey('backAddress','hoo',runtext)

                runtext = '배송시 요청사항 무작위 생성'
                delivery_request = desktopWeb.randomnumber(5,runtext,2)

                runtext = '배송시 요청사항 선택'
                desktopWeb.idSelectby('deliveryRequestCode',0,delivery_request,runtext)

                runtext = '배송지 추가하기 > 저장하기 버튼 선택'
                desktopWeb.xpathKey('//*[@id="addressForm"]/div/button[2]','enter',runtext)
                time.sleep(2)

                runtext = '배송지 변경 > 선택 버튼 선택'
                desktopWeb.xpathClick('/html/body/div[1]/div[3]/div/div/div[1]/ul/li[1]/div/div[6]/form/button[2]',runtext)
                time.sleep(1)

                runtext = '기존 Frame 변경'
                desktopWeb.frameSwitchOrginal(runtext)
                time.sleep(1)

                runtext = '선택한 주소로 배송지 변경 알럿'
                alert = desktopWeb.xpathCheck('//*[@id="addressConfirm"]/div/div[2]/button[2]',runtext)

                if alert == 'n':

                    runtext = '선택한 주소로 배송지 변경 알럿 > 확인 선탠'
                    desktopWeb.xpathKey('//*[@id="addressConfirm"]/div/div[2]/button[2]','enter',runtext)
                time.sleep(1)

        # 옵션 상품
        elif goods_Name == 25:

            if option == 1:

                runtext = '선택형'
                desktopWeb.optional_type(0,runtext)

            elif option == 2:

                runtext = '선택형1'
                desktopWeb.optional_type(0,runtext)

                runtext = '선택형2'
                desktopWeb.optional_type(1,runtext)
            
            elif option == 3:

                runtext = '선택형1'
                desktopWeb.optional_type(0,runtext)

                runtext = '선택형2'
                desktopWeb.optional_type(1,runtext)

                runtext = '선택형3'
                desktopWeb.optional_type(2,runtext)
            
            if text == 1:

                pass

            elif text == 2:

                runtext = '텍스트'
                desktopWeb.text_type(runtext)
            
            if calculation == 1:

                pass

            elif calculation == 2:
                
                runtext = '계산형'
                desktopWeb.calculation_type(runtext)
            
            if addtion == 1:

                pass

            elif addtion == 2:

                runtext = '추가구성'
                desktopWeb.additional_composition(runtext)

    # 쿠폰
    def coupons(self):

        goods_discount = self.goods_discount
        double_discount = self.double_discount
        coupon = self.coupon
        discount = self.discount
        goods_Number = self.goods_Number
        VIP_num = 0

        while VIP_num < 2:

            if goods_discount == 1 or goods_discount == 2 or goods_discount == 3 or double_discount == 1 or double_discount == 2 or double_discount == 3:
                
                runtext = '+ 선택'
                desktopWeb.xpathClick('//*[@id="coreSelectedLi_0"]/div[2]/span[1]/button[1]',runtext)
                time.sleep(1)

                runtext = '- 선택'
                desktopWeb.xpathClick('//*[@id="coreSelectedLi_0"]/div[2]/span[1]/button[2]',runtext)
                time.sleep(1)

                runtext = '쿠폰적용 버튼 선택'
                desktopWeb.xpathClick('//*[@id="coreSelectedLi_0"]/div[2]/span[2]/button',runtext)
                time.sleep(5)

                runtext = '쿠폰레이어창 확인'
                visible = desktopWeb.xpathWait('//*[@id="sCouponList"]',runtext)

                if visible == 0:

                    VIP_error = 33

                    runtext = '쿠폰 list'
                    list_value = desktopWeb.tagNames('li',runtext)
                    list_number = len(list_value)   

                    if double_discount == 1 or double_discount == 2 or double_discount == 3:
                        coupon_price = coupon
                    elif goods_discount == 1 or goods_discount == 2 or goods_discount == 3:
                        coupon_price = discount

                    if int(coupon_price) > 10:
                        pass
                    else:
                        coupon_price = str(coupon_price)+'%'                
                    coupon_price = str(coupon_price)
                    print(coupon_price)

                    n = 0
                    nn = 1
                    while n < list_number:
                                    
                        nn = str(nn)
                        runtext = '쿠폰 이름 추출'
                        coupon_name = desktopWeb.xpathReturnText('//*[@id="sCouponList"]/dd/ul/li['+nn+']/label/span[2]',runtext)
                        coupon_name = str(coupon_name).strip()

                        if goods_discount == 1 or double_discount == 1:

                            if '바이어' in coupon_name and coupon_price in coupon_name:

                                VIP_error = 0
                                break

                        elif goods_discount == 2 or double_discount == 2 :

                            if '마케팅' in coupon_name and coupon_price in coupon_name:
                                
                                VIP_error = 0
                                break
                        
                        elif goods_discount == 3 or double_discount == 3: 

                            if '펀딩' in coupon_name and coupon_price in coupon_name:
                                
                                VIP_error = 0
                                break

                        n = n + 1
                        nn = int(nn)
                        nn = nn + 1
                    
                    if VIP_error == 33:
                        
                        print('조건에 맞는 쿠폰이 존재하지 않아 진행 불가능 쿠폰을 다시 확인해 주세요')
                        common.desktopWebClose()
                        break
                    
                    else:

                        runtext = '쿠폰 선택'
                        desktopWeb.xpathClick('//*[@id="sCouponList"]/dd/ul/li['+str(nn)+']',runtext)
                        time.sleep(1)

                        runtext = '경고창 제어'
                        desktopWeb.alerClose(runtext)

                        runtext = '쿠폰적용 버튼 선택'
                        desktopWeb.xpathClick('//*[@id="layer_couponbox"]/div[3]/div[4]/a',runtext)
                        time.sleep(1)

                        VIP_error = 0
                        VIP_num += 5

                elif visible == 1:

                    VIP_error = 3
                    if VIP_num == 0:

                        print('쿠폰창 오류로 인해 재시도')
                        runtext = '페이지 새로고침'
                        desktopWeb.webrefresh(runtext)
                        time.sleep(3)

                        VIP.merchandise(self)
                        VIP.goods_num(self)
                        time.sleep(1)
                    
                    elif VIP_num != 0:

                        print('쿠폰 오류로 인해 진행 불가능')
                        common.desktopWebClose()

            else:

                VIP_error = 0
                VIP_num += 5
            
            VIP_num += 1

        return VIP_error

    # 구매수량
    def goods_num(self):

        goods_buyNumber = self.goods_buyNumber

        goods_buyNumber = str(goods_buyNumber)
        runtext = '수량 삭제'
        desktopWeb.xpathKey('//*[@id="coreSelectedLi_0"]/div[2]/span[1]/input','clear',runtext)
        time.sleep(1)

        runtext = '수량 기입'
        desktopWeb.xpathKey('//*[@id="coreSelectedLi_0"]/div[2]/span[1]/input',goods_buyNumber,runtext)
        time.sleep(1)

        runtext = '수량 확인'
        desktopWeb.xpathKey('//*[@id="coreSelectedLi_0"]/div[2]/span[1]/input','enter',runtext)
        time.sleep(1)

    # 구매하기 버튼 선택 > 주문서 화면 진입
    def buy_Button(self):
        
        Member = self.Member
        VIP_error = 0
        VIP_num = 0

        while VIP_num < 2:

            time.sleep(2)
            runtext = 'VIP > 구매하기 버튼 선택'
            desktopWeb.idKey('coreInsOrderBtn','enter',runtext)
            time.sleep(2)

            #일시적인 문제로 주문서 진입 불가 얼랏 제어 -> 장바구니로 우회 진입
            runtext = '경고창 제어'
            error = desktopWeb.alerClose(runtext)
            if error == None:

                VIP_num += 1

                if Member == 2:

                    runtext = '로그인 화면 > 비회원으로 구매하기 선택'
                    desktopWeb.idClick('nonMemberOrder',runtext)

            else:

                print('구매하기 버튼 선택 -> 주문서 진입 불가능 장바구니로 우회 시도')
                time.sleep(2)

                runtext = 'VIP > 장바구니 버튼 선택'
                desktopWeb.idKey('coreAddCartBtn','enter',runtext)
                time.sleep(1)

                runtext = 'VIP > 장바구니로 버튼 선택'
                desktopWeb.xpathClick('//*[@id="layer_mycart"]/div/div/div/div[2]/button[2]',runtext)
                time.sleep(2)

                runtext = '장바구니 >상품 link'
                link = desktopWeb.cssSelectorReturnAttribute('div.section.item_title > a','href',runtext)

                runtext = '장바구니 > 전체선택 확인'
                runtexttext = '장바구니 > 전체선택'
                allcheck = desktopWeb.xpathSelected('//*[@id="item_all_select"]',runtext,runtexttext)

                if allcheck == 0:

                    pass
                
                else:
                    
                    if VIP_num == 0:

                        runtext = '장바구니 > 전체선택 선택'
                        desktopWeb.xpathClick('//*[@id="cart_option"]/div/div/ul/li[1]/span/label',runtext)
                        time.sleep(1)

                runtext = '장바구니 > 선택삭제 버튼 선택'
                desktopWeb.classNameClick('btn_del',runtext)
                time.sleep(1)

                runtext = '경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = 'VIP > 상품 재진입'
                desktopWeb.webaddressConnect(link,runtext)
                time.sleep(3)

                try:

                    VIP.merchandise(self)
                    VIP.goods_num(self)
                    VIP.coupons(self)
                    time.sleep(2)
                
                except:

                    VIP_error = 5

                if VIP_error == 0:

                    runtext = 'VIP > 장바구니 버튼 선택'
                    desktopWeb.idKey('coreAddCartBtn','enter',runtext)
                    time.sleep(2)

                    runtext = 'VIP > 장바구니로 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="layer_mycart"]/div/div/div/div[2]/button[2]',runtext)
                    time.sleep(3)

                    runtext = '장바구니 > 구매하기 버튼 선택'
                    desktopWeb.xpathKey('//*[@id="cart_order"]/div/div[5]/div/div[2]/button','enter',runtext)
                    time.sleep(3)

                    runtext = '경고창 제어'
                    error = desktopWeb.alerClose(runtext)

                    if error == None:

                        time.sleep(5)
                        runtext = '경고창 제어'
                        error = desktopWeb.alerClose(runtext)
                        
                        if error == None:

                            if Member == 2:

                                runtext = '로그인 화면 > 비회원으로 구매하기 선택'
                                desktopWeb.idClick('nonMemberOrder',runtext)
                            
                            VIP_num += 5
   
                        else:

                            print('주문서 오류로 인해 진행 불가능')
                            VIP_error = 5
                            common.desktopWebClose()
                            break


                    else:
                        
                        print('주문서 진입 불가능')
                        VIP_error = 5
                        common.desktopWebClose()
                        break
            
            VIP_num += 1

        return VIP_error

    # 판매자 할인/아이템 할인 확인
    def SI_discount_check(self):

        goods_Price = self.goods_Price
        goods_discount = self.goods_discount
        discount = self.discount
        goods_Number = self.goods_Number
        VIP_error = 0

        goods_Price = int(goods_Price)
        discount = int(discount)

        if goods_discount == 4 or goods_discount == 6:

            runtext = '상품 금액 추출'
            x = desktopWeb.xpathReturnText("//strong[@class='price_real']",runtext)

            x = x.replace(',','')
            x = x.replace('원','')
            x = int(x)

            if discount > 10:

                y = goods_Price - discount

                if x != y:

                    VIP_error = 6
            
            else:

                z = goods_Price * discount / 100
                a , b = divmod(z,10)
                z = a * 10
                y = goods_Price - z

                if x != y:

                    VIP_error = 6
                    common.desktopWebClose()
        
        return VIP_error

    # 복수구매할인 확인
    def M_discount_check(self):

        goods_Price = self.goods_Price
        goods_discount = self.goods_discount
        discount = self.discount
        goods_buyNumber = self.goods_buyNumber
        goods_Number = self.goods_Number
        goods_Price = int(goods_Price)
        discount = int(discount)
        goods_buyNumber = int(goods_buyNumber)
        VIP_error = 0

        if goods_discount == 5:

            runtext = '복수구매할인 금액 추출'
            x = desktopWeb.xpathReturnText('//*[@class="text__unit-price"]/strong',runtext)
            if x == '없음':

                VIP_error = 7 
            
            else:

                x = x.replace(',','')
                x = x.replace('원','')
                x = x.replace('-','')
                x = int(x)

                if discount > 10:

                    y = discount * goods_buyNumber

                    if y != x:

                        VIP_error = 7
                
                else:

                    z = goods_Price * discount / 100
                    a , b = divmod(z,10)
                    z = a * 10
                    y = z * goods_buyNumber

                    if y != x:

                        VIP_error = 7
                        common.desktopWebClose()
        
        return VIP_error

    # VIP 통합본 version1(할인 체크 함)
    def consolidated_VIP1(self):

        Member = self.Member

        #판매자예치금 상품(쿠폰X,구매X)
        if Member == 6:
            
            pass

        #판매자예치금 상품(쿠폰X,구매X)
        else:
            
            n = 0
            while n < 1:

                VIP.itemdiscount(self)
                check = VIP.VIP_move(self)

                if check == 1:

                    print('환경적인 이슈(VIP화면오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
                    break

                check = VIP.SI_discount_check(self)

                if check == 6:

                    print('판매자할인 금액 오류로 자동화테스트 실패, ESM을 다시 확인해주세요.')
                    break

                check = VIP.login_process(self)

                if check == 2:

                    print('환경적인 이슈(로그인 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
                    break
                
                check = VIP.M_discount_check(self)

                if check == 7:

                    print('복수구매할인 금액오류로 자동화테스트 실패, ESM을 다시 확인해주세요.')

                VIP.merchandise(self)
                VIP.goods_num(self)

                check = VIP.coupons(self)

                if check == 3:

                    print('환경적인 이슈(쿠폰창 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
                    break
                
                elif check == 33:

                    print('조건에 맞는 쿠폰이 존재하지 않아 자동화테스트 실패, 쿠폰을 다시 확인해주세요.')
                    break
                
                check = VIP.buy_Button(self)

                if check == 5:

                    print('조건에 맞는 쿠폰이 존재하지 않아 자동화테스트 실패, 쿠폰을 다시 확인해주세요.')
                    break
                
                n += 1
        
        return check

class Checkout():

    def __init__(self,Member,goods_Name,smileCash,goods_smileCash,goods_Delivery,goods_discount,discount,goods_buyMethod,goods_Number):

        self.Member = Member
        self.goods_Name = goods_Name
        self.smileCash = smileCash
        self.goods_smileCash = goods_smileCash
        self.goods_Delivery = goods_Delivery
        self.goods_discount = goods_discount
        self.discount = discount
        self.goods_buyMethod = goods_buyMethod
        self.goods_Number = goods_Number

    # 배송지 변경
    def address_change(self):

        Member = self.Member
        goods_Name = self.goods_Name
        goods_Delivery = self.goods_Delivery
        checkout_error = 0
        Checkout_num = 0

        while Checkout_num < 2:

            # 비회원
            if Member == 2:

                #주문자정보
                runtext = '주문서 > 전체동의 선택'
                desktopWeb.xpathClick('//*[@id="content"]/div/div[2]/section/div/div/ul[1]/li/div/label',runtext)

                runtext = '주문서 > 주문자정보 > 주문자 기입'
                desktopWeb.idKey('xo_id_buyer_name','아무나',runtext)

                runtext = '주문서 > 주문자정보 > 연락처 기입'
                desktopWeb.idKey('xo_id_buyer_phone_number','01012345678',runtext)

                runtext = '주문서 > 주문자정보 > 이메일주소 기입'
                desktopWeb.idKey('xo_id_buyer_email','example@naver.com',runtext)

                runtext = '주문서 > 주문자정보 > 주문 비밀번호 기입'
                desktopWeb.idKey('xo_id_non_member_password','abced12345',runtext)

                runtext = '주문서 > 주문자정보 > 비밀번호 확인 기입'
                desktopWeb.idKey('xo_id_non_member_password_confirm','abced12345',runtext)

                # 타이어장착 or 방문수령 상품 
                if goods_Name == 6 or goods_Name == 8:

                    checkout_error = 0
                    Checkout_num += 5

                else:

                    # 배송지정보
                    runtext = '주문서 > 배송지정보 > 주문자 정보와 동일 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="content"]/div/div[1]/div[2]/div/div/div[2]/label',runtext)

                    runtext = '주문서 > 배송지정보 > 주소찾기 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="content"]/div/div[1]/div[2]/div/div/div[5]/button',runtext)

                    runtext = 'Frame 변경'
                    desktopWeb.frameSwitch(runtext)

                    runtext = '주소찾기창'
                    visible = desktopWeb.xpathCheck('//*[@id="container"]/div/div/button',runtext)

                    if visible == 'n':
                        
                        # 기본(=서울)
                        if goods_Delivery == 1:

                            runtext = '주소찾기 > 주소기입'
                            desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/form/input','강남파이낸스센터',runtext)

                            runtext = '주소찾기 > 돋보기 버튼 선택'
                            desktopWeb.xpathClick('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/button[2]',runtext)
                            time.sleep(1)

                            runtext = '주소찾기 > 검색한 주소 선택'
                            desktopWeb.xpathClick('//*[@id="1_0"]/a[2]',runtext)
                            time.sleep(1)

                            runtext = '주소찾기 > 이 위치로 배송지 설정 버튼 선택'
                            # # desktopWeb.imageClick(Gmarket_path+'delivery_setting.png',runtext)
                            desktopWeb.jsClick('//*[@id="container"]/div/div/div[1]/div[4]/div[2]/a/span',runtext)

                            runtext = '기존 Frame 변경'
                            desktopWeb.frameSwitchOrginal(runtext)

                            runtext = '주문서 > 배송지정보 > 상세주소 기입'
                            desktopWeb.idKey('xo_id_address_2','ㄹㅇ',runtext)

                            runtext = '요청사항 무작위 생성'
                            delivery_request = desktopWeb.randomnumber(5,runtext,2)

                            runtext = '주문서 > 배송지정보 > 요청사항 선택'
                            desktopWeb.idSelectby('delivery-request',0,delivery_request,runtext)

                        # 제주도
                        elif goods_Delivery == 2:

                            runtext = '주소찾기 > 주소기입'
                            desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/form/input','제주도',runtext)

                            runtext = '주소찾기 > 돋보기 버튼 선택'
                            desktopWeb.xpathClick('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/button[2]',runtext)
                            time.sleep(1)

                            runtext = '주소찾기 > 검색한 주소 선택'
                            desktopWeb.xpathClick('//*[@id="1_0"]/a[2]',runtext)
                            time.sleep(1)

                            runtext = '주소찾기 > 이 위치로 배송지 설정 버튼 선택'
                            # # desktopWeb.imageClick(Gmarket_path+'delivery_setting.png',runtext)
                            desktopWeb.jsClick('//*[@id="container"]/div/div/div[1]/div[4]/div[2]/a/span',runtext)

                            runtext = '기존 Frame 변경'
                            desktopWeb.frameSwitchOrginal(runtext)

                            runtext = '주문서 > 배송지정보 > 상세주소 기입'
                            desktopWeb.idKey('xo_id_address_2','ㄹㅇ',runtext)

                            runtext = '요청사항 무작위 생성'
                            delivery_request = desktopWeb.randomnumber(5,runtext,2)

                            runtext = '주문서 > 배송지정보 > 요청사항 선택'
                            desktopWeb.idSelectby('delivery-request',0,delivery_request,runtext)

                        # 도서산간
                        elif goods_Delivery == 3:

                            runtext = '주소찾기 > 주소기입'
                            desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/form/input','울릉도',runtext)

                            runtext = '주소찾기 > 돋보기 버튼 선택'
                            desktopWeb.xpathClick('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/button[2]',runtext)
                            time.sleep(1)

                            runtext = '주소찾기 > 검색한 주소 선택'
                            desktopWeb.xpathClick('//*[@id="1_0"]/a[2]',runtext)
                            time.sleep(2)
                        
                            runtext = '주소찾기 > 이 위치로 배송지 설정 버튼 선택'
                            # # desktopWeb.imageClick(Gmarket_path+'delivery_setting.png',runtext)
                            desktopWeb.jsClick('//*[@id="container"]/div/div/div[1]/div[4]/div[2]/a/span',runtext)
                            

                            runtext = '기존 Frame 변경'
                            desktopWeb.frameSwitchOrginal(runtext)

                            runtext = '주문서 > 배송지정보 > 상세주소 기입'
                            desktopWeb.idKey('xo_id_address_2','ㄹㅇ',runtext)

                            runtext = '요청사항 무작위 생성'
                            delivery_request = desktopWeb.randomnumber(5,runtext,2)

                            runtext = '주문서 > 배송지정보 > 요청사항 선택'
                            desktopWeb.idSelectby('delivery-request',0,delivery_request,runtext)

                        checkout_error = 0
                        Checkout_num += 5

                    else:
                        
                        checkout_error = 1

                        if Checkout_num == 0: 

                            print('배송지 오류로 인한 재시도')
                            runtext = '새로고침'
                            desktopWeb.webrefresh(runtext)
                            time.sleep(3)
                        
                        elif Checkout_num != 0:

                            print('배송지 오류로 인해 진행 불가능')
                            print('자동화 종료')
                            common.desktopWebClose()

            # 판매자회원
            elif Member == 6:

                checkout_error = 0
                Checkout_num += 5

            # 일반/클럽/사업자/SFC
            else:

                # 방문수령 or 타이어상품 
                if goods_Name == 8 or goods_Name == 6:

                    checkout_error = 0
                    Checkout_num += 5

                else:
                    
                    runtext = '주문서 > 배송지 > 배송지 변경 버튼 선택'
                    desktopWeb.idClick('xo_id_open_address_book',runtext)
                    time.sleep(1)

                    runtext = 'Frame 변경'
                    desktopWeb.frameSwitch(runtext)

                    runtext = '배송지 변경창'
                    visible = desktopWeb.xpathCheck('//*[@id="content"]/div[1]/button',runtext)

                    if visible == 'n':

                        runtext = '배송지 없는 경우 확인'
                        runtexttext = '배송지 없는 경우'
                        xx = desktopWeb.idDisplayed('address_nolist',runtext,runtexttext)

                        if xx == 1:

                            runtext = '배송지 List 확인'
                            yy = desktopWeb.idclassnameElement('ulAddressList','list-item',runtext)
                            
                            n = 1
                            while n < yy + 1:
                                
                                runtext = '배송지 이름 추출'
                                zz = desktopWeb.xpathText('//*[@id="ulAddressList"]/li['+str(n)+']/div[1]/div[1]/span[2]',runtext)
                                print(zz)

                                if goods_Delivery == 1:

                                    if '서울' in zz:

                                        break
                                
                                elif goods_Delivery == 2:

                                    if '제주' in zz:

                                        break

                                elif goods_Delivery == 3:

                                    if '도서' in zz:

                                        break
                                
                                n += 1
                            
                            runtext = '배송지 고유 id값 추출'
                            ww = desktopWeb.xpathReturnAttribute('//*[@id="ulAddressList"]/li['+str(n)+']/div[1]/div[6]/form','id',runtext)

                            if ww != '없음':

                                runtext = '배송지 선택 버튼 선택'
                                desktopWeb.xpathClick('//*[@id="'+str(ww)+'"]/button[2]',runtext)
                            
                            else:

                                runtext = '배송지 변경 > 배송지 추가하기 버튼 선택'
                                desktopWeb.xpathKey('//*[@id="content"]/div[1]/button','enter',runtext)
                                time.sleep(1)

                                runtext = '배송지 추가하기 > 배송지명 삭제'
                                desktopWeb.idKey('deliveryName','clear',runtext)
                                time.sleep(1)

                                if goods_Delivery == 1:

                                    runtext = '배송지 추가하기 > 배송지명 기입'
                                    desktopWeb.idKey('deliveryName','auto-서울',runtext)
                                
                                elif goods_Delivery == 2:

                                    runtext = '배송지 추가하기 > 배송지명 기입'
                                    desktopWeb.idKey('deliveryName','auto-제주도',runtext)
                                
                                elif goods_Delivery == 3:

                                    runtext = '배송지 추가하기 > 배송지명 기입'
                                    desktopWeb.idKey('deliveryName','auto-도서산간',runtext)
                                time.sleep(1)

                                runtext = '배송지 추가하기 > 받는 분 이름 기입'
                                desktopWeb.idKey('reciverName','아무나',runtext)
                                time.sleep(1)

                                runtext = '배송지 추가하기 > 받는 분 연락처 기입'
                                desktopWeb.idKey('hpNo','01012345678',runtext)
                                time.sleep(1)

                                runtext = '배송지 추가하기 > 주소 선택'
                                desktopWeb.xpathClick('//*[@id="beforeSearch"]/div/div/button',runtext)
                                time.sleep(1)

                                runtext = 'Frame 변경'
                                desktopWeb.frameSwitch(runtext)
                                
                                if goods_Delivery == 1:

                                    runtext = '주소찾기 > 주소 입력'
                                    desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/form/input','강남파이낸스센터',runtext)
                                    time.sleep(1)
                                
                                elif goods_Delivery == 2:

                                    runtext = '주소찾기 > 주소 입력'
                                    desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/form/input','제주도',runtext)
                                    time.sleep(1)
                                
                                elif goods_Delivery == 3:

                                    runtext = '주소찾기 > 주소 입력'
                                    desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/form/input','울릉도',runtext)
                                    time.sleep(1)
                                
                                runtext = '주소찾기 > 돋보기 선택'
                                desktopWeb.xpathKey('//*[@id="container"]/div/div/div[1]/div[1]/div[1]/button[2]','enter',runtext)
                                
                                runtext = '주소 찾기 > 주소 선택'
                                desktopWeb.xpathClick('//*[@id="1_0"]/a[2]/p[1]',runtext)
                                
                                runtext = '이 위치로 배송지 설정 선택'
                                desktopWeb.jsClick('//*[@id="container"]/div/div/div[1]/div[4]/div[2]/a',runtext)
                                time.sleep(2)

                                runtext = '기존 Frame 변경'
                                desktopWeb.frameSwitchOrginal(runtext)

                                runtext = 'Frame 변경'
                                desktopWeb.frameSwitch(runtext)

                                runtext = '배송지 추가하기 > 상세주소 기입'
                                desktopWeb.idKey('backAddress','hoo',runtext)

                                runtext = '배송시 요청사항 무작위 생성'
                                delivery_request = desktopWeb.randomnumber(5,runtext,2)

                                runtext = '배송시 요청사항 선택'
                                desktopWeb.idSelectby('deliveryRequestCode',0,delivery_request,runtext)

                                runtext = '배송지 추가하기 > 저장하기 버튼 선택'
                                desktopWeb.xpathKey('//*[@id="addressForm"]/div/button[2]','enter',runtext)
                                time.sleep(2)

                                runtext = '배송지 변경 > 선택 버튼 선택'
                                desktopWeb.xpathClick('/html/body/div[1]/div[3]/div/div/div[1]/ul/li[1]/div/div[6]/form/button[2]',runtext)
                                time.sleep(1)

                                runtext = '기존 Frame 변경'
                                desktopWeb.frameSwitchOrginal(runtext)
                                time.sleep(1)

                            checkout_error = 0
                            Checkout_num += 5

                        elif xx == 0:

                            checkout_error = 1

                            if Checkout_num == 0: 

                                print('배송지 오류로 인한 재시도')
                                runtext = '새로고침'
                                desktopWeb.webrefresh(runtext)
                                time.sleep(3)
                            
                            elif Checkout_num != 0:

                                print('배송지 오류로 인해 진행 불가능')
                                print('자동화 종료')
                                common.desktopWebClose()

                    else:

                        checkout_error = 1 

                        if Checkout_num == 0: 

                            print('배송지 오류로 인한 재시도')
                            runtext = '새로고침'
                            desktopWeb.webrefresh(runtext)
                            time.sleep(3)
                        
                        elif Checkout_num != 0:

                            print('배송지 오류로 인해 진행 불가능')
                            print('자동화 종료')
                            common.desktopWebClose()
    
        Checkout_num += 1
        time.sleep(5)

        return checkout_error

    # 스마일배송
    def smile_delivery(self):

        goods_discount = self.goods_discount

        if goods_discount == 23 or goods_discount == 24:

            runtext = '스마일 배송 선택'
            desktopWeb.xpathClick('//*[@id="xo_id_fast_delivery_request_details"]/div/div[2]/ul/li[2]/label',runtext)

    # 스마일프레시
    def smile_fresh(self):

        goods_Name =self.goods_Name

        if goods_Name == 27:

            time.sleep(2)
            runtext = 'Frame 변경'
            desktopWeb.frameSwitch(runtext)

            runtext = '주문서 > 배송시간 선택 > 이 시간으로 구매하기 선택'
            desktopWeb.xpathKey('//*[@id="layer--date-select"]/div/div[3]/button','enter',runtext)
            time.sleep(1)

            runtext = '기존 Frame 변경'
            desktopWeb.frameSwitchOrginal(runtext)

            runtext = '주문서 > 배송 상세정보 수정 버튼 선택'
            desktopWeb.xpathKey('//*[@id="content"]/div/div[1]/div[1]/div/div/div[3]/div[2]/div/button','enter',runtext)
            time.sleep(1)

            runtext = 'Frame 변경'
            desktopWeb.frameSwitch(runtext)

            runtext = '주문서 > 새벽배송 상세정보 > 상품 받을실 장소 선택'
            desktopWeb.idClick('form__radio1',runtext)

            runtext = '주문서 > 새벽배송 상세정보 > 공동현관 출입번호 > 비밀번호 없이 출입가능 선택'
            desktopWeb.xpathClick('//*[@id="doorLocationDetailBox"]/ul/li[2]/label',runtext)

            runtext = '주문서 > 새벽배송 상세정보 > 도착알림 선택'
            desktopWeb.xpathClick('//*[@id="content"]/section/div[1]/div[4]/ul/li[1]/label',runtext)

            runtext = '주문서 > 새벽배송 상세정보 > 이용 동의 필수 선택'
            desktopWeb.idClick('deliveryInfoAgree',runtext)

            runtext = '주문서 > 새벽배송 상세정보 > 저장하기 버튼 선택'
            desktopWeb.xpathKey('//*[@id="addressForm"]/div/button[2]','enter',runtext)
            time.sleep(1)

            runtext = '기존 Frame 변경'
            desktopWeb.frameSwitchOrginal(runtext)
            
    # Smile Cash 사용
    def smi_cash(self):

        Member = self.Member
        smileCash = self.smileCash
        goods_smileCash = self.goods_smileCash
        checkout_error = 0
        Checkout_num = 0

        while Checkout_num < 2:
            
            # 스마일캐시 N
            if smileCash == 0:

                Checkout_num += 5
            
            # 스마일캐시 Y
            elif smileCash == 1:

                # 비회원
                if  Member == 2:

                    Checkout_num += 5

                else:

                    try:

                        runtext = '주문서 > 할인 밎 스마일캐시 사용 > 스마일캐시 금액 기입'
                        desktopWeb.xpathKey('//*[@class="box__point box__smilecash"]/div[1]/div[1]/input',goods_smileCash,runtext)
                    
                    except:

                        checkout_error = 2

                        if Checkout_num == 0: 

                            print('스마일캐시 오류')
                            print('재시도')
                            runtext = '새로고침'
                            desktopWeb.webrefresh(runtext)
                            time.sleep(3)

                            try:

                                Checkout.payment_method(self)
                                Checkout.card_halin(self)

                            except:

                                checkout_error == 2
                                print('스마일캐시 오류로 인해 진행 불가능')
                                common.desktopWebClose()
                                break
                        
                        elif Checkout_num != 0:

                            print('스마일캐시 오류로 인해 진행 불가능')
                            print('자동화 종료')
                            common.desktopWebClose()
                            
            Checkout_num += 1

        return checkout_error

    # 카드사 즉시할인
    def card_halin(self):

        goods_discount = self.goods_discount
        discount = self.discount
        checkout_error = 0
        Checkout_num = 0

        while Checkout_num < 2:

            try:

                if goods_discount == 7:

                    runtext = '주문서 > 할인 및 스마일캐시 사용 > 카드사할인 추출'
                    card_list = desktopWeb.xpathReturnText('//*[@class="box__partner-card-wrap"]/div[1]/div[1]/div[1]/select',runtext)
                    card_list = card_list.split('\n')
                    n = len(card_list)
                    nn = 0
                    nnn = 0
                    while nn < n:
                        nnn = 2
                        if str(discount) in card_list[nn]:
                            nnn = 1
                            break

                        nn = nn + 1

                    if nnn == 2:

                        checkout_error = 33
                        print('조건에 맞는 카드사즉시할인이 존재하지 않아 진행 불가능 카즉할인을 다시 확인해 주세요')
                        common.desktopWebClose()
                        break
                    
                    elif nnn == 1:

                        runtext = '주문서 > 할인 및 스마일캐시 사용 > 카드사할인 선택'
                        desktopWeb.xpathSelectby('//*[@class="box__partner-card-wrap"]/div[1]/div[1]/div[1]/select',2,nn,runtext)

                        runtext = '주문서 > 할인 및 스마일캐시 사용 > 사용하기 버튼 선택'
                        desktopWeb.xpathKey('//*[@class="box__partner-card-wrap"]/div[1]/button','enter',runtext)
                        checkout_error = 0
                        Checkout_num += 5

                else:

                    checkout_error = 0
                    Checkout_num += 5

            except:
                
                checkout_error = 3

                if Checkout_num == 0:

                    print('카드사 즉시할인 오류')
                    print('재시도')

                    runtext = '새로고침'
                    desktopWeb.webrefresh(runtext)
                    time.sleep(3)

                    try:

                        Checkout.payment_method(self)
                
                    except:

                        checkout_error = 3
                        print('카드사 즉시할인 오류로 인해 진행 불가능')
                        common.desktopWebClose()
                        break
                
                elif Checkout_num != 0:

                    print('카드사 즉시할인 오류로 인해 진행 불가능')
                    print('자동화 종료')
                    common.desktopWebClose()

            Checkout_num += 1

        return checkout_error

    #결제수단
    def payment_method(self):

        Member = self.Member
        goods_buyMethod = self.goods_buyMethod

        card_random = 5

        # 사업자회원 X and 간편결제
        if Member != 5 and 6 <= goods_buyMethod <= 11:
            
            # SFC 회원
            if Member == 4:

                n = 1
                while n < 7:

                    n = str(n)
                    try:

                        runtext = '주문서 > 결제수단 > 간편결제'
                        spm = desktopWeb.xpathReturnAttribute('//*[@class="list__payment"]/li['+n+']','class',runtext)
                        spm = str(spm)
                        print(spm)

                        #캐시       
                        if spm == 'box__card-bg box__bank box__smilecash auto-charge':
                            a = n
                            a = int(a)
                        #신용카드
                        elif spm == 'box__card-bg   card30002 sprite__payment-card':
                            b = n
                            b = int(b)
                        #계좌이체
                        elif spm == 'box__card-bg box__bank bank30012   sprite__payment-card':
                            c = n
                            c = int(c)
                        else:
                            d = 8
                            e = 9
                            f = 10
                    except:
                        pass
                    n = int(n)
                    n = n + 1 
            
            else:

                n = 2
                while n < 11:
                    n = str(n)
                    try:

                        runtext = '주문서 > 결제수단 > smilepay 결제수단'
                        spm = desktopWeb.xpathReturnAttribute('//*[@class="list__payment"]/li['+n+']/div/div|//*[@class="box__pay-view"]/div/div[2]/ul/li['+n+']/div/div|//*[@id="xo_id_section_smile_pay"]/div[2]/div/div[2]/ul/li['+n+']/div/div[1]','class',runtext)
                        spm = str(spm)
                        print(spm)

                        #캐시       
                        if spm == 'box__card-bg box__bank box__smilecash auto-charge':
                            a = n
                            a = int(a)
                        #신용카드
                        elif spm == 'box__card-bg   card30006 sprite__payment-card':
                            b = n
                            b = int(b)
                        #계좌이체
                        elif spm == 'box__card-bg box__bank bank30012   sprite__payment-card':
                            c = n
                            c = int(c)
                        #T1
                        elif spm == 'box__card-bg   card30084 box__plcc':
                            d = n
                            d = int(d)
                        #T2
                        elif spm == 'box__card-bg   card30085 box__plcc':
                            e = n
                            e = int(e)
                        #휴대폰
                        elif spm == 'box__card-bg  box__phone phone30053  sprite__payment-card':
                            f =n
                            f = int(f)
                        else:
                            pass
                    except:
                        pass
                    n = int(n)
                    n = n + 1 

        # 판매자 예치금
        elif Member == 6:

            pass

        else:

            runtext = '주문서 > 결제수단 > 일반 결제 선택'
            desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[1]/label',runtext)

        
        # 스마일페이 - 캐시충전/T1/T2/신용/계좌/휴대폰  
        # 일반결제 - 신용/현금/휴대폰/온누리
        # 판매자 예치금  - 신용/무통장
        n = 0
        nn = 0
        # 간편결제 
        if 6 <= goods_buyMethod <= 11:

            # 캐시충전결제
            if goods_buyMethod == 6:

                nn = 0

            # 신용/체크카드
            elif goods_buyMethod == 9:

                nn = b - 1

            # 은행 계좌이체
            elif goods_buyMethod == 10:

                nn = c - 1

            # T1
            elif goods_buyMethod == 7:

                nn = d - 1

            # T2
            elif goods_buyMethod == 8:

                nn = e - 1

            # 휴대폰 결제
            elif goods_buyMethod == 11:

                nn = f - 1
            
            print(nn)
            time.sleep(2)

            runtext = '주문서 > 결제수단 > 간편결제 > 뒤로가기 버튼'
            runruntext = '주문서 > 결제수단 > 간편결제 >  뒤로가기 버튼 선택'
            arrow = desktopWeb.xpathClickSkip('//*[@id="xo_id_section_smile_pay"]/div[2]/div/button[1]',runtext,runruntext)
            if arrow == 'p':

                pass

            elif arrow == 'n':

                nn = nn - 1
            
            print(nn)
            time.sleep(2)

            while n < nn:

                    runtext = '주문서 > 결제수단 > 간편결제 > 다음버튼 선택'
                    desktopWeb.xpathClick('//*[@id="xo_id_section_smile_pay"]/div[2]/div/button[2]',runtext)
                    time.sleep(1)
                    n = n + 1
            
        # 일반결제
        elif 1 <= goods_buyMethod <= 5:

            runtext = '일반결제 list_tab 확인'
            num = desktopWeb.xpathclassnameElement('//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul','list-item',runtext)
            paylist = 1
            while paylist < num + 1:

                paylist = str(paylist)
                runtext = '일반결제 list 추출'
                paylist_name = desktopWeb.xpathReturnAttribute('//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li['+paylist+']/input','id',runtext)
                if paylist_name == 'pay_chk_CreditCard':
                    pay_position_card = '//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li['+paylist+']/label'
                elif paylist_name == 'pay_chk_ForeignCreditCard':
                    pay_position_Forecard = '//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li['+paylist+']/label'
                elif paylist_name == 'pay_chk_VirtualAccount':
                    pay_position_bank = '//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li['+paylist+']/label'
                elif paylist_name == 'pay_chk_Mobile':
                    pay_position_mobile = '//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li['+paylist+']/label'
                elif paylist_name == 'pay_chk_Paypal':
                    pay_position_paypal = '//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li['+paylist+']/label'
                paylist = int(paylist)
                paylist += 1

            #신용 - 국민, 신한만 사용(현대,삼성 사용 불가)
            if goods_buyMethod == 1:

                runtext = '주문서 > 결제수단 > 일반결제 > 신용/체크카드 선택'
                desktopWeb.xpathClick(pay_position_card,runtext)

                runtext = '카드 선택 랜덤값'
                card_random = desktopWeb.randomnumber(3,runtext,2)
                card_random = "2"

                runtext  = '주문서 > 결제수단 > 일반결제 > 신용/체크카드 > 카드 선택'
                desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li['+card_random+']',runtext)
                card_random = int(card_random)

            # 무통장 입급 - 우체국으로 고정
            elif goods_buyMethod == 2:

                runtext = '주문서 > 결제수단 > 일반결제 > 무통장 입급 선택'
                desktopWeb.xpathClick(pay_position_bank,runtext)

                runtext = '주문서 > 결제수단 > 일반결제 > 무통장 입급 > 우체국 선택'
                desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[6]',runtext)

                # 비회원
                if Member == 2:

                    runtext = '주문서 > 결제수단 > 일반결제 > 무통장 입급 > 우체국 > 계좌번호 기입'
                    desktopWeb.idKey('xo_id_refund_account_number','0123456789',runtext)
                    time.sleep(1)

                    runtext = '주문서 > 결제수단 > 일반결제 > 무통장 입급 > 우체국 > 예금주명 기입'
                    desktopWeb.idKey('xo_id_refund_account_owner_name','아무나',runtext)
                    time.sleep(1)

                    runtext = '주문서 >  결제수단 > 일반결제 > 무통장 입급 > 우체국 > 계좌확인 선택'
                    desktopWeb.idClick('xo_id_refund_account_confirm_button',runtext)

                    runtext = '경고창 제어'
                    desktopWeb.alerClose(runtext)
                
                # 간편회원
                elif Member == 3:

                    runtext = '주문서 > 결제수단 > 일반결제 > 무통장 입급 >  우체국 > 계좌번호 기입'
                    desktopWeb.idKey('xo_id_refund_account_number','0123456789',runtext)

                    runtext = '주문서 > 결제수단 > 일반결제 > 무통장 입급 > 우체국 > 계좌확인 선택'
                    desktopWeb.idClick('xo_id_refund_account_confirm_button',runtext)

                    runtext = '경고창 제어'
                    desktopWeb.alerClose(runtext)

            # 휴대폰
            elif goods_buyMethod == 3:
                
                runtext = '주문서 > 결제수단 > 일반결제 > 휴대폰 소액결제 선택'
                desktopWeb.xpathClick(pay_position_mobile,runtext)

                runtext = '주문서 > 결제수단 > 일반결제 > 휴대폰 소액결제 > SKT 선택'
                desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[1]',runtext)

            # 온누리(제외)
            elif goods_buyMethod == 4:

                pass

        # 판매자 예치금
        elif 13 <= goods_buyMethod <= 17:

            runtext = '판매자 예치금 주문결제 진입'
            desktopWeb.webaddressConnect('https://checkout-dev.gmarket.co.kr/server/ko/pc/gate/goCheckout?type=seller-deposit',runtext)
            time.sleep(2)

            # 판매자 예치금 충전
            runtext = '판매자 예치금 랜덤값 생성'
            depost_radio = desktopWeb.randomnumber(5,runtext)

            runtext = '주문결제 > 판매자 예치금 충전 > radiobutton 선택'
            desktopWeb.xpathClick('//*[@id="wrapper"]/div/div/section/div/div[1]/ul/li['+depost_radio+']',runtext)

            # 결제수단
            # 신용/체크카드
            if 13 <= goods_buyMethod <= 16:

                runtext = '주문결제 > 결제수단 > 신용/체크카드 선택'
                desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li[1]/label',runtext)

                # 현대
                if goods_buyMethod == 13:

                    runtext = '주문결제 > 결제수단 > 신용/체크카드 > 현대카드 선택'
                    # desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[1]',runtext)
                    desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[3]',runtext)

                # 국민
                elif goods_buyMethod == 14:

                    runtext = '주문결제 > 결제수단 > 신용/체크카드 > KE국민카드 선택'
                    desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[2]',runtext)

                # 삼성
                elif goods_buyMethod == 15:

                    runtext = '주문결제 > 결제수단 > 신용/체크카드 > 삼성카드 선택'
                    # desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[4]',runtext)
                    desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[3]',runtext)
                
                # 신한
                elif goods_buyMethod == 16:

                    runtext = '주문결제 > 결제수단 > 신용/체크카드 > 신한카드 선택'
                    desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li[3]',runtext)

            # 무통장(하나은행 제외)
            elif goods_buyMethod == 17:

                runtext = '주문결제 > 결제수단 > 무통장 입급 선택'
                desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/ul/li[2]/label',runtext)

                runtext = '통장 선택 랜덤값 생성'
                bank_number = desktopWeb.randomnumber(6,runtext)
                
                runtext = '주문결제 > 결제수단 > 무통장 입급 > 은행 선택'
                desktopWeb.xpathClick('//*[@id="xo_id_section_normal_pay"]/div[2]/div/div/div/ul/li['+bank_number+']',runtext)
            
        else:
            
            pass
        
        return card_random

    # 결제하기 선택
    def last_buy(self):

        Member = self.Member
        goods_Number = self.goods_Number
        Checkout_num = 0

        runtext = '스크린 샷'
        desktopWeb.webScreenshot('Gmarket_dev/screenshot/'+goods_Number+'주문서','//*[@class="section__right"]',runtext)

        while Checkout_num < 2:

            # 결제하기
            # 판매자예치금
            if Member == 6:

                runtext = '주문결제 > 결제하기 선택'
                desktopWeb.xpathKey('//*[@id="wrapper"]/div/div/section/div/button','enter',runtext)
            
            else:

                runtext = '주문결제 > 결제하기 선택'
                desktopWeb.xpathKey('//*[@id="content"]/div/div[2]/div/div[2]/div/div/button','enter',runtext)
            time.sleep(2)

            runtext = '이 배송지 맞나요? 알럿'
            alert = desktopWeb.xpathCheck('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/button[2]',runtext)

            if alert == 'n':

                runtext = '이 배송지 맞나요?'
                desktopWeb.xpathKey('/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/div/div/button[2]','enter',runtext)
            
            else:

                pass
            print('결제창 진입')

            runtext = '경고창 제어'
            error = desktopWeb.alerClose(runtext)

            if error == None:

                checkout_error = 0
                Checkout_num += 5
            
            else:

                checkout_error = 5

                if Checkout_num == 0:

                    print('결제하기 오류')
                    print('재시도')
                    runtext = '새로고침'
                    desktopWeb.webrefresh(runtext)
                    time.sleep(3)

                    try:

                        Checkout.payment_method(self)
                        Checkout.card_halin(self)
                        Checkout.smi_cash(self)

                    except:

                        checkout_error = 5
                        print('결제하기 오류로 인해 진행 불가능')
                        common.desktopWebClose()
                        break
                
                elif Checkout_num != 0:
                    
                    print('결제하기 오류로 인해 진행 불가능')
                    print('자동화종료')
                    common.desktopWebClose()

        Checkout_num += 1

        return checkout_error

    #결제창
    def payment(self,card_random):

        goods_buyMethod = self.goods_buyMethod
        goods_Name = self.goods_Name
        goods_discount = self.goods_discount
        smileCash = self.smileCash
        checkout_error = 0
        Checkout_num = 0
        handphon = '' # 휴대폰 번호 기입
        danal_phone_pw = '' # 휴대폰 간편 결제 번호 기입(휴대폰번호 + 간편결제 등록된 번호만 써놓을 것)
        kb_pw = '' # KB 간편 결제 비밀번호 기입
        # 신한 카드 비번의 경우 2112에 가서 기입할 것 
        

        time.sleep(5)

        while Checkout_num < 2:

            # 스마일페이 보안 번호 입력
            if 6 <= goods_buyMethod <= 11 or (goods_buyMethod == 2 and smileCash == 1):

                runtext = 'Frame 전환'
                frame = desktopWeb.frameSwitch(runtext)
                
                """
                (695,705) <-> (1207,975) 큰 사각형 가로 522 세로 270  작은 사각형 가로 128 세로 90
                배율 125 % 해상도 1920 X 1080 기준 !!!
                new_imagesmilePay는 스마일페이 보안 결제 전용 나머지는 쓰지말것 
                """
                # 스마일 페이 결제의 경우 원하는 숫자를 기입할 것 ex) 0을 입력시 0.png
                runtext = '숫자 선택'
                desktopWeb.new_imagesmilePay('number',smilepay_path+'.png',runtext,1/2,1/2,0.9)

                runtext = '숫자 선택'
                desktopWeb.new_imagesmilePay('number',smilepay_path+'.png',runtext,1/2,1/2,0.9)

                runtext = '숫자 선택'
                desktopWeb.new_imagesmilePay('number',smilepay_path+'.png',runtext,1/2,1/2,0.9)

                runtext = '숫자 선택'
                desktopWeb.new_imagesmilePay('number',smilepay_path+'.png',runtext,1/2,1/2,0.9)
 
                runtext = '숫자 선택'
                desktopWeb.new_imagesmilePay('number',smilepay_path+'.png',runtext,1/2,1/2,0.9)

                runtext = '숫자 선택'
                desktopWeb.new_imagesmilePay('number',smilepay_path+'.png',runtext,1/2,1/2,0.9)

                time.sleep(6)

                checkout_error = 0
                Checkout_num += 5

            # 신용/체크 카드(판매자 예치금 신용/체크카드 포함)
            elif goods_buyMethod == 1 or 13 <= goods_buyMethod <= 16:

                # 국민카드
                if card_random == 2:
                    
                    # SFC몰 상품 / PCS할인
                    if goods_Name == 20 or goods_discount == 8:

                        runtext = '결제 팝업창 제어'
                        desktopWeb.popupControl(2,runtext)

                    else:

                        runtext = '결제 팝업창 제어'
                        desktopWeb.popupControl(1,runtext)
                    time.sleep(3)

                    runtext = 'KB 국민카드 > ISP 인증서 결제 선택'
                    desktopWeb.xpathClick('//*[@id="tabView01"]/div[2]/div/div[2]/button',runtext)
                    time.sleep(10)

                    # SFC몰 상품 / PCS할인
                    if goods_Name == 20 or goods_discount == 8:

                        runtext = '기존창으로 전환'
                        desktopWeb.popupControl(1,runtext)

                    else:

                        runtext = '기존창으로 전환'
                        desktopWeb.popupOrginal(runtext)
                    time.sleep(3)

                    # ISP 제어
                    # runtext = 'UiRobot.exe 실행'
                    # UiRobot = common.findfile("UiRobot.exe", "/",runtext)
                    # UiRobot = UiRobot.replace('UiRobot.exe','UiRobot')
                    # uiallpath = UiRobot +' -f '+kbcard_path

                    # runtext = 'uipath 실행'
                    # common.filerunRun(uiallpath,runtext)
                    # time.sleep(8)

                    runtext = 'KB 국민카드 > 결제비밀번호 선택'
                    desktopWeb.imageClick(kbcard_path+'isp.png',runtext)

                    runtext = 'KB 국민카드 > 결제비밀번호 기입'
                    desktopWeb.webPyautoguiWrite(kb_pw,runtext)

                    runtext = 'KB 국민카드 > 결제진행 선택'
                    desktopWeb.imageClick(kbcard_path+'ispbuy.png',runtext)

                    runtext = 'KB 국민카드 > X버튼 선택'
                    desktopWeb.imageClick(kbcard_path+'kbkb.png',runtext,95/100,1/2,0.6)
                    time.sleep(5)

                # 신한카드
                # //*[@id="nppfs-keypad-smartId"]/div/div[2]/img[] -> img[] 에 숫자 기입 ex)//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[10]
                # 개인 신한카드 기입 할 것 
                elif card_random == 3:

                    # SFC몰 상품 / PCS할인
                    if goods_Name == 20 or goods_discount == 8:

                        runtext = '결제 팝업창 제어'
                        desktopWeb.popupControl(2,runtext)

                    else:

                        runtext = '결제 팝업창 제어'
                        desktopWeb.popupControl(1,runtext)
                    time.sleep(3)

                    runtext = '신한카드 > 다른결제 선택'
                    desktopWeb.xpathClick('//*[@id="fanView"]/div[2]/ul/li[2]',runtext)
                    time.sleep(1)

                    runtext = '신한카드 > 패스워드 결제 선택'
                    desktopWeb.xpathClick('//*[@id="otherView"]/div[3]/ul/li[4]',runtext)
                    time.sleep(1)

                    runtext = '신한카드 > 패스워드 결제 > 마우스 버튼 선택'
                    desktopWeb.idClick('e2e_smartId_useyn_toggle',runtext)
                    time.sleep(1)
                    
                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)

                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)

                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)


                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)

                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)

                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)


                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)

                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)


                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)

                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[2]/img[]',runtext)
                    time.sleep(3)

                    runtext = '신한카드 > 패스워드 결제 >  키보드 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="nppfs-keypad-smartId"]/div/div[4]/img[]',runtext)
                    time.sleep(1)

                    runtext = '신한카드 > 패스워드 결제 > 확인버튼 선택'
                    desktopWeb.idClick('btnConfirm',runtext)
                    time.sleep(2)

                    runtext = '확인버튼 선택'
                    desktopWeb.idClick('btnNext',runtext)

                    # SFC몰 상품 / PCS할인
                    if goods_Name == 20 or goods_discount == 8:

                        runtext = '기존창으로 전환'
                        desktopWeb.popupControl(1,runtext)

                    else:

                        runtext = '기존창으로 전환'
                        desktopWeb.popupOrginal(runtext)

                Checkout_num += 5

            # 무통장 입급 - 우체국
            elif goods_buyMethod == 2 and smileCash == 0:

                 Checkout_num += 5

            # 휴대폰 결제 - skt
            elif goods_buyMethod == 3:
                
                time.sleep(5)

                #휴대폰 결제창
                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)
                time.sleep(5)

                runtext = '오류 확인'
                result = desktopWeb.xpathReturnText('/html/body/span/h1',runtext)

                if '오류' in result:

                    checkout_error = 6

                    if Checkout_num == 0:

                        print('휴대폰 결제창 오류')
                        print('재시도')

                        runtext = '새로고침'
                        desktopWeb.webrefresh(runtext)
                        time.sleep(3)

                        try:

                            Checkout.payment_method(self)
                            Checkout.card_halin(self)
                            Checkout.smi_cash(self)
                            Checkout.last_buy(self)

                        except:

                            print('결제 수단 오류로 인한 결제 불가능')
                            print('자동화 종료')
                            common.desktopWebClose()
                            break
                    
                    elif Checkout_num != 0:

                        print('결제 수단 오류로 인한 결제 불가능')
                        print('자동화 종료')
                        common.desktopWebClose()
                        break

                else:

                    # KG 모빌리언스
                    runtext = 'KG 모빌리언스 결제창 확인'
                    KG = desktopWeb.xpathCheck('//*[@id="mcashForm"]/div/div[1]/div[1]/div[1]/img',runtext)

                    if KG == 'n':

                        runtext = 'KG 모빌리언스 > 휴대폰 인증'
                        runruntext = 'KG 모빌리언스 > 휴대폰 번호 기입'
                        exist = desktopWeb.idKeySkip('phoneNo2',handphon,runtext,runruntext)

                        if exist == 'p':

                            runtext = 'KG 모빌리언스 > 다음버튼 선택'
                            desktopWeb.idClick('easyNextBtn1',runtext)
                                 
                        try:
                            n = 1
                            nn = 0 
                            while n < 7:

                                n = str(n)
                                runtext = 'KG 모빌리언스 > 숫자 0 추출'
                                number = desktopWeb.xpathReturnText('//*[@id="xkeyboard"]/table/tbody/tr[1]/td['+n+']/a/em',runtext)
                                print(number)
                                
                                number = int(number)

                                if number == nn:

                                    break

                                n = int(n)
                                n = n + 1
                            n = str(n)

                            nnn = 0
                            while nnn < 6:

                                runtext = 'KG 모빌리언스 > 숫자 선택'
                                desktopWeb.xpathClick('//*[@id="xkeyboard"]/table/tbody/tr[1]/td['+n+']/a/em',runtext)
                                nnn = nnn + 1
                            time.sleep(3)

                            checkout_error = 0
                            Checkout_num += 5
                        
                        except:
                            
                            nnn = 0
                            while nnn < 6:

                                runtext = 'KG 모빌리언스 > 숫자 선택'
                                desktopWeb.xpathClick('//*[@id="xkeyboard"]/table/tbody/tr[1]/td[1]',runtext)
                                nnn = nnn + 1
                            time.sleep(3)

                            checkout_error = 0
                            Checkout_num += 5

                    
                    else:

                        # Danal
                        runtext = 'Danal 결제창 확인'
                        Danal = desktopWeb.idCheck('ID_ISTITLE',runtext)

                        if Danal == 'n':

                            runtext = 'Danal > 휴대폰 간편결제 선택'
                            desktopWeb.idClick('ID_AREA_SELECT_EASYPAY_OPEN',runtext)
                            time.sleep(1)

                            runtext = 'Danal > 휴대폰 간편결제 > 결제하기 선택'
                            desktopWeb.xpathClick('//*[@id="ID_AREA_SELECT_EASYPAY"]/span/button[2]',runtext)
                            time.sleep(1)

                            runtext = 'Danal > 휴대폰 기입'
                            desktopWeb.idKey('ID_DST_ADDR',handphon,runtext)

                            runtext = 'Danal > 다음버튼 선택'
                            desktopWeb.idClick('ID_BTN_NEXT_CHK_USERINFO',runtext)
                            time.sleep(1)
                        
                            runtext = 'Danal > 간편결제 비밀번호 기입'
                            desktopWeb.idKey('ID_EASY_PASS_INPUT',danal_phone_pw,runtext)

                            runtext = 'Danal > 결제 버튼 선택'
                            desktopWeb.jsClick('//*[@id="ID_BTN_NEXT_CHK_PASSWORD"]',runtext)
                            time.sleep(3)

                            checkout_error = 0
                            Checkout_num += 5

                        # BillGate
                        else:

                            phone = 0
                            while phone < 7:

                                runtext = 'BillGate >  취소 버튼 선택'
                                desktopWeb.jsClick('//*[@id="section_agree2"]/div[2]/a[1]',runtext)

                                runtext = 'Frame 전환'
                                desktopWeb.frameSwitchOrginal(runtext)

                                Checkout.payment_method(self)

                                Checkout.last_buy(self)
                                time.sleep(1)

                                runtext = 'Frame 전환'
                                desktopWeb.frameSwitch(runtext)
                                time.sleep(5)

                                runtext = '오류 확인'
                                result = desktopWeb.xpathReturnText('/html/body/span/h1',runtext)

                                if '오류' in result:

                                    checkout_error = 6
                                    phone = 8
                                
                                else:

                                    runtext = 'KG 모빌리언스 결제창 확인'
                                    KG = desktopWeb.xpathCheck('//*[@id="mcashForm"]/div/div[1]/div[1]/div[1]/img',runtext)

                                    if KG == 'n':

                                        phone = 8
                                    
                                    else:

                                        runtext = 'Danal 결제창 확인'
                                        Danal = desktopWeb.idCheck('ID_ISTITLE',runtext)

                                        if Danal == 'n':

                                            phone = 8
                                
                                phone += 1
                                    
                            time.sleep(5)

                            #휴대폰 결제창
                            runtext = 'Frame 전환'
                            desktopWeb.frameSwitch(runtext)
                            time.sleep(5)

                            runtext = '오류 확인'
                            result = desktopWeb.xpathReturnText('/html/body/span/h1',runtext)

                            if '오류' in result:

                                checkout_error = 6

                                if Checkout_num == 0:

                                    print('휴대폰 결제창 오류')
                                    print('재시도')

                                    runtext = '새로고침'
                                    desktopWeb.webrefresh(runtext)
                                    time.sleep(3)

                                    try:

                                        Checkout.payment_method(self)
                                        Checkout.card_halin(self)
                                        Checkout.smi_cash(self)
                                        Checkout.last_buy(self)

                                    except:

                                        print('결제 수단 오류로 인한 결제 불가능')
                                        print('자동화 종료')
                                        common.desktopWebClose()
                                        break
                                
                                elif Checkout_num != 0:

                                    print('결제 수단 오류로 인한 결제 불가능')
                                    print('자동화 종료')
                                    common.desktopWebClose()
                                    break

                            else:

                                # KG 모빌리언스
                                runtext = 'KG 모빌리언스 결제창 확인'
                                KG = desktopWeb.xpathCheck('//*[@id="mcashForm"]/div/div[1]/div[1]/div[1]/img',runtext)

                                if KG == 'n':

                                    runtext = 'KG 모빌리언스 > 휴대폰 인증'
                                    runruntext = 'KG 모빌리언스 > 휴대폰 번호 기입'
                                    exist = desktopWeb.idKeySkip('phoneNo2',handphon,runtext,runruntext)

                                    if exist == 'p':

                                        runtext = 'KG 모빌리언스 > 다음버튼 선택'
                                        desktopWeb.idClick('easyNextBtn1',runtext)
                                                           
                                    try:
                                        n = 1
                                        nn = 0 
                                        while n < 7:

                                            n = str(n)
                                            runtext = 'KG 모빌리언스 > 숫자 0 추출'
                                            number = desktopWeb.xpathReturnText('//*[@id="xkeyboard"]/table/tbody/tr[1]/td['+n+']/a/em',runtext)
                                            print(number)
                                            
                                            number = int(number)

                                            if number == nn:

                                                break

                                            n = int(n)
                                            n = n + 1
                                        n = str(n)

                                        nnn = 0
                                        while nnn < 6:

                                            runtext = 'KG 모빌리언스 > 숫자 선택'
                                            desktopWeb.xpathClick('//*[@id="xkeyboard"]/table/tbody/tr[1]/td['+n+']/a/em',runtext)
                                            nnn = nnn + 1
                                        time.sleep(3)

                                        checkout_error = 0
                                        Checkout_num += 5
                                    
                                    except:
                                        
                                        nnn = 0
                                        while nnn < 6:

                                            runtext = 'KG 모빌리언스 > 숫자 선택'
                                            desktopWeb.xpathClick('//*[@id="xkeyboard"]/table/tbody/tr[1]/td[1]',runtext)
                                            nnn = nnn + 1
                                        time.sleep(3)

                                        checkout_error = 0
                                        Checkout_num += 5

                                
                                else:

                                    # Danal
                                    runtext = 'Danal 결제창 확인'
                                    Danal = desktopWeb.idCheck('ID_ISTITLE',runtext)

                                    if Danal == 'n':

                                        runtext = 'Danal > 휴대폰 간편결제 선택'
                                        desktopWeb.idClick('ID_AREA_SELECT_EASYPAY_OPEN',runtext)
                                        time.sleep(1)

                                        runtext = 'Danal > 휴대폰 간편결제 > 결제하기 선택'
                                        desktopWeb.xpathClick('//*[@id="ID_AREA_SELECT_EASYPAY"]/span/button[2]',runtext)
                                        time.sleep(1)

                                        runtext = 'Danal > 휴대폰 기입'
                                        desktopWeb.idKey('ID_DST_ADDR',handphon,runtext)

                                        runtext = 'Danal > 다음버튼 선택'
                                        desktopWeb.idClick('ID_BTN_NEXT_CHK_USERINFO',runtext)
                                        time.sleep(1)
                                        
                                        runtext = 'Danal > 간편결제 비밀번호 기입'
                                        desktopWeb.idKey('ID_EASY_PASS_INPUT',danal_phone_pw,runtext)

                                        runtext = 'Danal > 결제 버튼 선택'
                                        desktopWeb.jsClick('//*[@id="ID_BTN_NEXT_CHK_PASSWORD"]',runtext)
                                        time.sleep(3)

                                        checkout_error = 0
                                        Checkout_num += 5

                            checkout_error = 0
                            Checkout_num += 5
            
            Checkout_num += 1
        time.sleep(5)

        return checkout_error

    # 주문서 통합본 version1
    def consolidated_Checkout(self):

        n = 0
        while n < 1:

            checkout_error = Checkout.address_change(self)

            if checkout_error == 1:
                print('환경적인 이슈(주소지변경창오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
                break

            card_random = Checkout.payment_method(self)

            checkout_error = Checkout.card_halin(self)

            if checkout_error == 3:
                print('환경적인 이슈(카드사 즉시할인 오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
                break
            
            elif checkout_error == 33:

                print('조건에 맞는 카드사할인이 존재하지 않아 자동화테스트 실패, 카드사 즉시할인 다시 확인 바랍니다.')
                break
            
            checkout_error = Checkout.smi_cash(self)

            if checkout_error == 2:

                print('환경적인 이슈(스마일캐시)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')

            checkout_error = Checkout.last_buy(self)

            if checkout_error == 5:

                print('환경적인 이슈(결제하기)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
                break

            checkout_error = Checkout.payment(self,card_random)

            if checkout_error == 6:

                print('환경적인 이슈(결제수단오류)로 인해 자동화테스트 실패, 다시 시도해주시길 바랍니다.')
                break
            
            n += 1

        return checkout_error

class Order_Completion():

    def __init__(self,goods_Number,goods_Name,goods_discount):

        self.goods_Number =goods_Number
        self.goods_Name = goods_Name
        self.goods_discount = goods_discount
    
    def order_completion(self):

        goods_Number = self.goods_Number
        goods_Name = self.goods_Name
        goods_discount = self.goods_discount

        #결제후 실패 alret
        runtext = '경고창 제어'
        error = desktopWeb.alerClose(runtext)

        runtext = '기존 Frame으로 전환'
        desktopWeb.frameSwitchOrginal(runtext)

        if error == None:

            nonono = 0
            print('주문완료창 진입')
            time.sleep(10)

            runtext = '주문완료 확인'
            result = desktopWeb.xpathReturnText('//*[@id="container"]/div[1]/h2',runtext)
            result = str(result)

            if result == '주문완료':

                desktopWeb.weballScreenshot('Gmarket_dev/screenshot/'+goods_Number+'Success','주문완료')

            elif result == '없음':

                nonono = 1
                desktopWeb.weballScreenshot('Gmarket_dev/screenshot/'+goods_Number+'Fail','주문완료창 진입 실패')
        
            elif '주문지연' in result:

                nonono = 2
                desktopWeb.webScreenshot('Gmarket_dev/screenshot/'+goods_Number+'Delay','//*[@id="container"]/div[2]','주문지연')


            else:

                nonono = 3
                desktopWeb.weballScreenshot('Gmarket_dev/screenshot/'+goods_Number+'Fail','주문실패')


        else:

            print('환경적인 오류로 인한 결제 실패')
            nonono = 11

        #PCS/SFC 제휴 삭제
        if goods_Name == 20 or goods_discount == 8:

            runtext = 'Chrome 설정창'
            desktopWeb.popupOrginal(runtext)
            time.sleep(3)

            runtext = '인터넷 사용 기록 삭제 선택'
            desktopWeb.imageClick(Chromesetting_path+'delete.png',runtext,1/2,1/2,0.8)

        # Item 할인 삭제
        if goods_discount == 6:

            core.swagger.item_discount(goods_Number,2,0)

        return nonono


