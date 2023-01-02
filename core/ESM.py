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
corepath=scriptpath+'/core'
browserpath=scriptpath+'/webdriver/'
DevAdminpath = scriptpath
DevAdmin_G9_path = scriptpath + '/img/DevAdmin_G9/'
DevAdmin_Contract_Status_path = scriptpath + '/img/DevAdmin_Contract_Status/'
ESM_path = scriptpath + '\\img\ESM\\'
sys.path.append(scriptpath)

# 라이브러리 참조하기
from core.lib import *
from core.config import *
from core.package import *
from core.testrail_api import *
from core.slack import *

"""
ESM 모듈 파일
Chrome 기준
ESM 1.0 / 2.0 상품 수정 가능
상품 가격, 상품 판매기간(자동으로 변경해줌), 판매자할인, 복수구매할인, 배송비 제어 가능
ESM 통합본은 크게 두 가지
ESM_check의 경우 본인이 설정한 값(테스트할 상품)과 ESM 값이 일치하는지 확인해주는 용도
ESM_modify의 경우 본인이 설정한 값(테스트할 상품)에 따라 ESM값들을 변경해주는 용도

"""

class ESM_controll:

    def __init__(self,esm_id,esm_pw):

        self.esm_id = esm_id
        self.esm_pw = esm_pw

    # 로그인
    def login(self,goods_Name):

        if goods_Name == 23 or goods_Name == 24:
            ID = 'hoyeon0808'
            PW = 'test1004!'
        
        else:
            ID = self.esm_id
            PW = self.esm_pw
        
        runtext = 'Chrome Browser 구동'
        desktopWeb.browserRun("Chrome",browserpath+'chromedriver',runtext)

        runtext = 'DEV ESM 접속'
        desktopWeb.webaddressConnect("https://www-dev.esmplus.com/Home/Home",runtext)
        time.sleep(1)

        runtext = '로그인 화면 > Gmaket 라디오 버튼 선택'
        desktopWeb.xpathClick("//div[@id='captchaLogin']/div/div/div/label[2]/input", runtext)

        runtext = '로그인 화면 > ID 입력'
        desktopWeb.idKey("SiteId",ID,runtext)
        time.sleep(1)

        runtext = '로그인 화면 > PW 입력'
        desktopWeb.idKey("SitePassword",PW,runtext)
        time.sleep(1)

        runtext = '로그인 화면 > 로그인 버튼 클릭'
        desktopWeb.idClick("btnSiteLogOn",runtext)
        time.sleep(5)

        runtext = '2단계 인증 '
        runtexttext = '2단계 인증 > X 버튼 선택'
        certified = desktopWeb.xpathClickSkip('//*[@id="layer-mfa"]/button',runtext,runtexttext)

        if certified == 'p':

            runtext = 'ESM Admin 접속'
            desktopWeb.webaddressConnect("http://admin-dev.esmplus.com/SignIn/LogOn?ReturnUrl=%2f",runtext)
            time.sleep(2)

            #로그인
            runtext = '로그인 화면 > 계정 입력'
            desktopWeb.idKey("Id","stc1594",runtext)
            time.sleep(1)

            runtext = '로그인 화면 > 비밀번호 입력'
            desktopWeb.idKey("Password","Ansghdubwkc12!?",runtext)
            time.sleep(1)

            runtext = '로그인 화면 > eBayKorea 계정사용 버튼 선택'
            desktopWeb.idClick('EbayKorea',runtext)

            runtext = '로그인 화면 > 로그인 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div/div/div/div/form/input',runtext)
            time.sleep(2)

            runtext = 'ESMadmin > ESM 관리 버튼 선택'
            desktopWeb.xpathClick('//*[@id="header"]/ul/li[7]',runtext)

            runtext = 'ESMadmin > ESM 관리 > 디버그 로그인 선택'
            desktopWeb.xpathClick('//*[@id="header"]/ul/li[7]/div/ul/li[1]',runtext)

            runtext = '아이디 기입'
            desktopWeb.idKey('txtId','test4plan',runtext)

            runtext = '접속 사유 기입'
            desktopWeb.idKey('txtReason','test',runtext)

            runtext = '로그인 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div/form/span[3]',runtext)
            time.sleep(1)

            common.desktopWebClose()
            time.sleep(4)
        
        else:

            runtext = '로그인 화면 오류 확인'
            f5 = desktopWeb.xpathCheck('//*[@id="contents"]/div/div/div/p',runtext)

            if f5 == 'n':
                
                runtext = '새로고침'
                desktopWeb.webrefresh(runtext)

            elif f5 == 'p':

                pass

            #대표번호 인증창
            runtext = '대표번호 인증'
            runtexttext = '대표번호 인증 > ESM+로 이동하기 버튼 클릭'
            desktopWeb.xpathClickSkip('//*[@id="l-content"]/div/div/div[6]/a/img',runtext,runtexttext)

            runtext = 'ESM 홈 > 상품등록/변경 노출 확인'
            result = desktopWeb.xpathCheck('//*[@id="TDM001"]/a',runtext)

            if result == 'n':

                pass

            elif result == 'p':

                runtext = 'ESM Admin 접속'
                desktopWeb.webaddressConnect("http://admin-dev.esmplus.com/SignIn/LogOn?ReturnUrl=%2f",runtext)
                time.sleep(2)

                #로그인
                runtext = '로그인 화면 > 계정 입력'
                desktopWeb.idKey("Id","stc1594",runtext)
                time.sleep(1)

                runtext = '로그인 화면 > 비밀번호 입력'
                desktopWeb.idKey("Password","Ansghdubwkc12!?",runtext)
                time.sleep(1)

                runtext = '로그인 화면 > eBayKorea 계정사용 버튼 선택'
                desktopWeb.idClick('EbayKorea',runtext)

                runtext = '로그인 화면 > 로그인 버튼 선택'
                desktopWeb.xpathClick('//*[@id="contents"]/div/div/div/div/form/input',runtext)

                runtext = 'ESMadmin > ESM 관리 버튼 선택'
                desktopWeb.xpathClick('//*[@id="header"]/ul/li[7]',runtext)

                runtext = 'ESMadmin > ESM 관리 > 디버그 로그인 선택'
                desktopWeb.xpathClick('//*[@id="header"]/ul/li[7]/div/ul/li[1]',runtext)

                runtext = '아이디 기입'
                desktopWeb.idKey('txtId','test4plan',runtext)

                runtext = '접속 사유 기입'
                desktopWeb.idKey('txtReason','test',runtext)

                runtext = '로그인 버튼 선택'
                desktopWeb.xpathClick('//*[@id="contents"]/div/form/span[3]',runtext)
                time.sleep(1)

                common.desktopWebClose()
                time.sleep(4)

    # ESM 홈
    def ESM_HOME(self):

        ID = self.esm_id
        PW = self.esm_pw

        runtext = 'Default 창 전환'
        desktopWeb.popupOrginal(runtext)

        runtext = 'ESM 홈 > 팝업창 제어'
        desktopWeb.popupClose(runtext)

        runtext = 'Layer 팝업'
        runtexttext = 'ESM 홈 > Layer 팝업 제어'
        desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

        runtext = '로그인 Layer 팝업'
        runtexttext = 'ESM 홈 > 로그인 Layer 팝업 제어'
        existence = desktopWeb.xpathClickSkip('/html/body/div[10]/div[3]/button',runtext,runtexttext)

        if existence =='P':

            ESM_controll.login(ID,PW)

            runtext = 'ESM 홈 > 팝업창 제어'
            desktopWeb.popupClose(runtext)

            runtext = 'Layer 팝업'
            runtexttext = 'ESM 홈 > Layer 팝업 제어'
            desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

        runtext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0 확인'
        runtexttext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0'
        result = desktopWeb.xpathDisplayed('//*[@id="TDM396"]/a',runtext,runtexttext)
        time.sleep(1)

        if result == 0:

            runtext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0 선택'
            desktopWeb.xpathClick('//*[@id="TDM396"]/a',runtext)
        
        elif result == 1:

            runtext = 'ESM 홈 > 상품등록/변경 선택'
            desktopWeb.xpathClick('//*[@id="TDM001"]/a',runtext)
            time.sleep(1)

            runtext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0 선택'
            desktopWeb.xpathClick('//*[@id="TDM396"]/a',runtext)
        time.sleep(2)

        runtext = '로그인 Layer 팝업'
        runtexttext = 'ESM 홈 > 로그인 Layer 팝업 제어'
        existence2 = desktopWeb.xpathClickSkip('/html/body/div[11]/div[3]/button',runtext,runtexttext)

        if existence2 =='P':

            ESM_controll.login(ID,PW)

            runtext = 'ESM 홈 > 팝업창 제어'
            desktopWeb.popupClose(runtext)

            runtext = 'Layer 팝업'
            runtexttext = 'ESM 홈 > Layer 팝업 제어'
            desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

            runtext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0 확인'
            runtexttext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0'
            result = desktopWeb.xpathDisplayed('//*[@id="TDM396"]/a',runtext,runtexttext)
            time.sleep(1)

            if result == 0:

                runtext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0 선택'
                desktopWeb.xpathClick('//*[@id="TDM396"]/a',runtext)
            
            elif result == 1:

                runtext = 'ESM 홈 > 상품등록/변경 선택'
                desktopWeb.xpathClick('//*[@id="TDM001"]/a',runtext)
                time.sleep(1)

                runtext = 'ESM 홈 > 상품등록/변경 > 상품관리2.0 선택'
                desktopWeb.xpathClick('//*[@id="TDM396"]/a',runtext)
            time.sleep(2)

    # ESM 상품관리 1.0,2.0
    def Goods_manage(self,number):

        runtext = 'Frame 전환'
        desktopWeb.frameSwitch(runtext)

        runtext = '오류'
        a = desktopWeb.xpathCheck('//*[@id="contents"]/div/div/div/strong/img',runtext)

        if a == 'p':

            pass

        elif a == 'n':

            runtext = '새로고침'
            desktopWeb.webrefresh(runtext)
            time.sleep(3)

            ESM_controll.ESM_HOME(self)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

        #상품관리 2.0 
        runtext = '상품관리2.0 > 상품번호 기입' 
        desktopWeb.xpathKey('//*[@id="txtGoodsId"]|//*[@class="textarea"]/textarea', number, runtext)
        time.sleep(1)

        runtext = '상품관리2.0 > 검색하기 버튼 선택'
        desktopWeb.xpathClick('//*[@id="imgItemsSearch"]',runtext)
        time.sleep(5)

        runtext = '상품관리 버전 확인'
        check = desktopWeb.xpathCheck('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img|//*[@class="x-grid-row user_modify"]/td[6]/div/a/img',runtext)
                                        
        if check == 'n':

            runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
            desktopWeb.xpathClick('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img|//*[@class="x-grid-row user_modify"]/td[6]/div/a/img',runtext)

        elif check == 'p':

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)

            runtext = 'ESM 홈 > 상품등록/변경 > 상품관리'
            desktopWeb.xpathClick('//*[@id="TDM100"]/a',runtext)
            time.sleep(2)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@id="contents"]/div/div/div/strong/img',runtext)

            if a == 'p':

                pass

            elif  a == 'n':

                runtext = '새로고침'
                desktopWeb.webrefresh(runtext)
                time.sleep(3)

                runtext = 'ESM 홈 > 팝업창 제어'
                desktopWeb.popupClose(runtext)

                runtext = 'Layer 팝업'
                runtexttext = 'ESM 홈 > Layer 팝업 제어'
                desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

            #상품관리 1.0
            runtext = '상품관리 > 상품번호 기입' 
            desktopWeb.cssSelectorKey('#txtGoodsIds', number, runtext)
            time.sleep(1)

            runtext = '상품관리 > 검색하기 버튼 선택'
            desktopWeb.xpathClick('//*[@id="imgItemsSearch"]',runtext)
            time.sleep(2)

            runtext = '상품관리 > 상품관리 > 상품 수정 버튼'
            runtexttext = '상품관리 > 상품관리 > 상품 수정 버튼 선택'
            chechec = desktopWeb.xpathClickSkip('//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img|//tbody/tr[2]/td[5]/div[1]/a[1]/img[1]',runtext,runtexttext)

            if chechec == 'n':

                check = 'nono'
            
        time.sleep(10)

        return check

    # 상품 판매기간 변경
    def Sales_period(check):

        # 2.0
        if check == 'n':

            runtext = '판매 종료 잔여일 확인'
            day = desktopWeb.xpathReturnText('//*[@id="sectionSellingPeriod"]/td/div/div/dl/dd/span[2]',runtext)
            day = int(day)

            if day == 0:

                runtext = '기본정보 > 판매기간 > 기간연장 선택'
                desktopWeb.idClick('chkExtendSellingPeriod',runtext)

                runtext = '기본정보 >  판매기간 > 판매기간 선택'
                desktopWeb.idSelectby('sltFixedPriceSellingPeriod',1,'90일',runtext)
            
            else:

                pass
        # 1.0
        elif check == 'p':

            runtext = '상품수정 > 판매기간 > 판매기간 확인'
            day = desktopWeb.xpathReturnText('//*[@id="sectionSellingPeriod"]/td/div/p[1]',runtext)
            day = day.split(':')[2]
            day = day.split('일')[0].strip()
            day = int(day)

            if day == 0:

                runtext = '상품수정 > 판매기간 >  기간연장 선택'
                desktopWeb.idClick('chkExtendSellingPeriod',runtext)

                runtext = '상품수정 > 판매기간 >  판매기간 선택'
                desktopWeb.idSelectby('sltFixedPriceSellingPeriod',1,'90일',runtext)
            
            else:

                pass

    # 상품 가격 확인
    def Price_Check(check,price):

        price_check = 0

        # 2.0
        if check == 'n':

            runtext = '기존 상품가격'
            result = desktopWeb.xpathReturnAttribute("//input[@name='txtGoodsPrice']",'value',runtext)
            time.sleep(1)

        # 1.0
        elif check == 'p':

            runtext = '기존 상품가격'
            result = desktopWeb.idReturnAttribute('txtGoodsPrice','value',runtext)
            time.sleep(1)

        if ',' in result:
            result = result.replace(',','')

        if int(price) == int(result):

            price_check = 0
        
        elif int(price) != int(result):

            price_check = 1

        return price_check

    # 상품 가격 변경
    def Price_Change(check,price):

        # 2.0
        if check == 'n':

            runtext = '기존 상품가격'
            result = desktopWeb.xpathReturnAttribute("//input[@name='txtGoodsPrice']",'value',runtext)
            time.sleep(1)

            runtext = '기존 상품가격 삭제'
            desktopWeb.xpathKey("//input[@name='txtGoodsPrice']",'clear',runtext)
            time.sleep(1)

            runtext = '상품가격 새 기입'
            desktopWeb.xpathKey("//input[@name='txtGoodsPrice']",price,runtext)

            runtext = '가격 변경 실수 방지 노출 확인'
            desktopWeb.xpathClick("//tr[@class='item item_goods-price']//div[@class='label']",runtext)
            time.sleep(2)

            runtext = '가격 변경 실수 방지 유무 확인'
            runtexttext = '가격변경 실수 방지 노출'
            price_Fluctuations = desktopWeb.xpathCheck("//div[@class='goods-price_change']",runtext)
            
            if price_Fluctuations == 'n': #큰 폭의 가격변동일때
                
                runtext = '가격'
                res = desktopWeb.xpathReturnText("//span[@class='change_write_sum']",runtext)

                runtext = '실수 방지 가격 기입'
                desktopWeb.xpathKey("//input[@class='change_write_sum']",res,runtext)

        # 1.0
        elif check == 'p':

            runtext = '기존 상품가격'
            result = desktopWeb.idReturnAttribute('txtGoodsPrice','value',runtext)

            runtext = '기존 상품가격 삭제'
            desktopWeb.idClear('txtGoodsPrice',runtext)

            runtext = '상품가격 새 기입'
            desktopWeb.idKey('txtGoodsPrice',price,runtext)
            print(result,' -> ',price.replace('000',',000'))

            runtext = '가격 변경 실수 방지 노출 확인'
            desktopWeb.xpathClick('//*[@id="sectionSellingPeriod"]/th/div',runtext)

            runtext = '가격 변경 실수 방지 유무 확인'
            runtexttext = '가격변경 실수 방지 노출'
            price_Fluctuations = desktopWeb.idDisplayed('divGoodsPriceConfirm',runtext,runtexttext)

            if price_Fluctuations == 0: #큰 폭의 가격변동일때

                runtext = '가격'
                res = desktopWeb.idReturnText('divGoodsPriceChnagedHangul',runtext)

                runtext = '실수 방지 가격 기입'
                desktopWeb.idKey('txtGoodsPriceChangedHangulConfirm',res,runtext)

            else:
                pass

        
        return result

    # 판매자 할인 확인
    def Seller_Discount_Check(check,gd,discount):

        seller_discount_check = 0

        # 2.0
        if check == 'n':

            if gd == 4:

                runtext = '판매자 부담할인 > 설정하기 버튼 선택'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'
                y_n = desktopWeb.idSelected('chkSellerDiscountIsUsed',runtext,runtexttext)

                if y_n == 0:

                    runtext = '판매자 부담할인 > 판매자 부담할인 추출'
                    x = desktopWeb.idReturnAttribute('SYIStep3_SellerDiscount_DiscountAmtGmkt|SYIStep3_SellerDiscount_DiscountAmt','value',runtext)

                    if ',' in x:
                        x = x.replace(',','')

                    if int(discount) == int(x):

                        seller_discount_check = 0
                    
                    elif int(discount) != int(x):

                        seller_discount_check = 1

                elif y_n == 1:

                    seller_discount_check = 1

        # 1.0
        elif check == 'p':

            if gd == 4:

                runtext = '판매자 부담할인 > 설정하기 버튼 선택'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'
                y_n = desktopWeb.idSelected('//*[@id="sectionSellerDiscount"]/td/div/div/label[2]/input',runtext,runtexttext)

                if y_n == 0:

                    runtext = '판매자 부담할인 > 판매자 부담할인 추출'
                    x = desktopWeb.idReturnAttribute('SYIStep3_SellerDiscount_DiscountAmt','value',runtext)

                    if ',' in x:
                        x = x.replace(',','')

                    if int(discount) == int(x):

                        seller_discount_check = 0
                    
                    elif int(discount) != int(x):

                        seller_discount_check = 1

                elif y_n == 1:

                    seller_discount_check = 1
                    
        return seller_discount_check

    # 판매자 할인 변경
    def Seller_Discount(check,gd,discount):

        discount = int(discount)
        # 2.0
        if check == 'n':

            if gd == 4:
                
                runtext = '판매자 부담할인 > 설정하기 버튼 선택'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'
                y_n = desktopWeb.idSelected('chkSellerDiscountIsUsed',runtext,runtexttext)

                if y_n == 0:

                    runtext = '설정하기 버튼 한번 선택'
                    desktopWeb.idClick('chkSellerDiscountIsUsed',runtext)

                    runtext = '설정하기 버튼 두번 선택'
                    desktopWeb.idClick('chkSellerDiscountIsUsed',runtext)

                elif y_n == 1:

                    runtext = '설정하기 버튼 선택'
                    desktopWeb.idClick('chkSellerDiscountIsUsed',runtext)
                
                if discount > 10:

                    runtext = '정액버튼 선택'
                    desktopWeb.xpathClick('//*[@id="spnSellerDiscount"]/label[1]/input[1]',runtext)

                    runtext = '할인율 기입'
                    desktopWeb.idKey('SYIStep3_SellerDiscount_DiscountAmt',discount,runtext)

                else:

                    runtext = '정율버튼 선택'
                    desktopWeb.xpathClick('//*[@id="spnSellerDiscount"]/label[2]/input[1]',runtext)

                    runtext = '할인율 기입'
                    desktopWeb.idKey('SYIStep3_SellerDiscount_DiscountAmt',discount,runtext)
                
            else:

                runtext = '판매자 부담할인 설정 안함'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'

                y_n = desktopWeb.idSelected('chkSellerDiscountIsUsed',runtext,runtexttext)

                if y_n == 0:

                    desktopWeb.idClick('chkSellerDiscountIsUsed',runtext)

                else:
        
                    pass

        # 1.0
        elif check == 'p':

            runtext = 'G9 동시등록요청 > G9 동시등록요청 안함 선택'
            desktopWeb.idClick('G9DualListing_N',runtext)

            if gd == 4:
                
                runtext = '판매자 부담할인 > 사용 버튼 선택'
                desktopWeb.xpathClick('//*[@id="sectionSellerDiscount"]/td/div/div/label[2]',runtext)

                discount = int(discount)
                if discount > 10:

                    runtext = '정액버튼 선택'
                    desktopWeb.xpathClick('//*[@id="spnSellerDiscount"]/label[1]',runtext)

                    runtext = '할인율 삭제'
                    desktopWeb.idKey('SYIStep3_SellerDiscount_DiscountAmt','clear',runtext)

                    runtext = '할인율 기입'
                    desktopWeb.idKey('SYIStep3_SellerDiscount_DiscountAmt',discount,runtext)

                else:

                    runtext = '정율버튼 선택'
                    desktopWeb.xpathClick('//*[@id="spnSellerDiscount"]/label[2]',runtext)

                    runtext = '할인율 삭제'
                    desktopWeb.idKey('SYIStep3_SellerDiscount_DiscountAmt','clear',runtext)

                    runtext = '할인율 기입'
                    desktopWeb.idKey('SYIStep3_SellerDiscount_DiscountAmt',discount,runtext)
                
            else:

                runtext = '판매자 부담할인 > 미사용 버튼 선택'
                desktopWeb.xpathClick('//*[@id="sectionSellerDiscount"]/td/div/div/label[1]',runtext)

    # 배송비 확인
    def delivery_Check(check,ss,gd,dc):

        if check == 'n':

            if dc == 1:
                # 무료, 유료/선결제, 유료/착불, 유료/착불&선결제, 조건부/착불&선결제, 조건부/선결제, 조건부/착불

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 확인'
                runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비'
                y_n = desktopWeb.idSelected('rdoDeliveryFeeType1',runtext,runtexttext)

                if y_n == 0:

                    if gd == 1:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 무료 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        if '무료' in x:
                            
                            delivery_check = 0
                        
                        else:

                            delivery_check = 1

                    elif gd == 2:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '유료' in x:
                            
                            if y == '선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 3:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '유료' in x:
                            
                            if y == '착불 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 4:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불&선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불&선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '유료' in x:
                            
                            if y == '착불&선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 5:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불&선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불&선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '조건부' in x:
                            
                            if y == '착불&선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 6:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '조건부' in x:
                            
                            if y == '선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 7:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '조건부' in x:
                            
                            if y == '착불 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1
                
                elif y_n == 1:

                    delivery_check = 1
            
            elif dc == 2:

                # 무료, 유료/선결제, 조건부/선결제, 수량별차등/구매수량별, 수량별차등/배송비구간
                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 확인'
                runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비'
                y_n = desktopWeb.idSelected('rdoDeliveryFeeType2',runtext,runtexttext)
                time.sleep(1)

                if y_n == 0:

                    if gd == 8:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 무료 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 무료'
                        x = desktopWeb.idSelected('rdoEachDeliveryFeeType1',runtext,runtexttext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1
                    
                    elif gd == 9:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 유료/선결제 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 유료/선결제'
                        x  = desktopWeb.idSelected('rdoEachDeliveryFeeType2',runtext,runtexttext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1

                    elif gd == 10:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 조건부/선결제 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 조건부/선결제'
                        x  = desktopWeb.idSelected('rdoEachDeliveryFeeType3',runtext,runtexttext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1

                    elif gd == 11:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 수량별차등/구매수량별 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 수량별차등/구매수량별'
                        x  = desktopWeb.idSelected('rdoEachDeliveryFeeType4',runtext,runtexttext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1

                    elif gd == 12:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 수량별차등/배송비구간 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 수량별차등/배송비구간'
                        x  = desktopWeb.idSelected('rdoEachDeliveryFeeType4',runtext,runtexttext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1

                elif y_n == 1:

                    delivery_check = 1

            else:

                if ss == 0:

                    if gd == 14 :

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 무료배송 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 무료배송'
                        x = desktopWeb.idSelected('TplDeliveryFree',runtext,runtexttext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1


                    elif gd == 13:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 유료배송 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 유료배송'
                        x = desktopWeb.idSelected('TplDeliveryFee',runtext,runtexttext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1

        elif check == 'p':
            
            if dc == 1:
            # 무료, 유료/선결제, 유료/착불, 유료/착불&선결제, 조건부/착불&선결제, 조건부/선결제, 조건부/착불

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 확인'
                runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비'
                y_n = desktopWeb.xpathSelected('rdoDeliveryFeeType1',runtext,runtexttext)

                if y_n == 0:
                
                    if gd == 1:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 무료 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        if '무료' in x:
                            
                            delivery_check = 0
                        
                        else:

                            delivery_check = 1
                        

                    elif gd == 2:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '유료' in x:
                            
                            if y == '선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 3:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '유료' in x:
                            
                            if y == '착불 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 4:
                                
                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불&선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 유료/착불&선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '유료' in x:
                            
                            if y == '착불&선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 5:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불&선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불&선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '조건부' in x:
                            
                            if y == '착불&선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 6:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/선결제 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/선결제 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '조건부' in x:
                            
                            if y == '선결제 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1

                    elif gd == 7:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불 확인'
                        x = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt1',runtext)

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 조건부/착불 확인'
                        y = desktopWeb.idReturnText('SelectedDeliveryFeeTemplateTxt3',runtext)

                        if '조건부' in x:
                            
                            if y == '착불 선택':

                                delivery_check = 0
                            
                            else:
                                
                                delivery_check = 1
                        
                        else:

                            delivery_check = 1
                
                elif y_n == 1:

                    delivery_check = 1
            
            else:
                # 무료, 유료/선결제, 조건부/선결제, 수량별차등/구매수량별, 수량별차등/배송비구간

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 확인'
                runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비'
                y_n = desktopWeb.idSelected('rdoDeliveryFeeType2',runtext,runtexttext)

                if y_n == 0:

                    if gd == 8:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 무료 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 무료'
                        x = desktopWeb.idClick('rdoEachDeliveryFeeType1',runtext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1
                    
                    elif gd == 9:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 유료/선결제 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 유료/선결제'
                        x = desktopWeb.idClick('rdoEachDeliveryFeeType2',runtext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1

                    elif gd == 10:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 조건부/선결제 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 조건부/선결제'
                        x = desktopWeb.idClick('rdoEachDeliveryFeeType3',runtext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1
                    
                    elif gd == 11:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 수량별차등/구매수량별 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 수량별차등/구매수량별'
                        x = desktopWeb.idClick('rdoEachDeliveryFeeType4',runtext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1
                        
                    elif gd == 12:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 수량별차등/배송비구간 확인'
                        runtexttext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 수량별차등/배송비구간'
                        x = desktopWeb.idClick('rdoEachDeliveryFeeType4',runtext)

                        if x == 0:

                            delivery_check == 0
                        
                        elif x == 1:

                            delivery_check == 1
                    
                elif y_n == 1:

                    delivery_check = 1

        return delivery_check

    # 배송비 설정
    def delivery(check,ss,gd,dc):

        if check == 'n':

            if dc == 1:
                # 무료, 유료/선결제, 유료/착불, 유료/착불&선결제, 조건부/착불&선결제, 조건부/선결제, 조건부/착불

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 출하지선택'
                desktopWeb.idSelectby('selShipmentPlaceNo',1,u'STA TEST11',runtext)
                time.sleep(3)

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 선택'
                desktopWeb.idClick('rdoDeliveryFeeType1',runtext)
                time.sleep(1)

                if gd == 1:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 무료'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'무료 (664208)',runtext)

                elif gd == 2:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 유료/선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'유료/2,500원/선결제 선택 (664234)',runtext)

                elif gd == 3:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 유료/착불'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'유료/2,500원/착불 선택 (664136)',runtext)

                elif gd == 4:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 유료/착불&선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'유료/5,000원/착불&선결제 선택 (664237)',runtext)

                elif gd == 5:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 조건부/착불&선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'조건부무료-50,000원 이상 무료/50,000원 미만 2500원/착불&선결제 선택 (664198)',runtext)

                elif gd == 6:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 조건부/선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'조건부무료-50,000원 이상 무료/50,000원 미만 2500원/선결제 선택 (664224)',runtext)

                elif gd == 7:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 조건부/착불'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'조건부무료-50,000원 이상 무료/50,000원 미만 3000원/착불 선택 (664273)',runtext)
            
            elif dc == 2:
                # 무료, 유료/선결제, 조건부/선결제, 수량별차등/구매수량별, 수량별차등/배송비구간

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 출하지선택'
                desktopWeb.idSelectby('selShipmentPlaceNo',1,u'STA TEST11',runtext)
                time.sleep(3)

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 선택'
                desktopWeb.idClick('rdoDeliveryFeeType2',runtext)
                time.sleep(1)

                if gd == 8:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 무료'
                    desktopWeb.idClick('rdoEachDeliveryFeeType1',runtext)
                
                elif gd == 9:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 유료/선결제'
                    desktopWeb.idClick('rdoEachDeliveryFeeType2',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.idClear('txtEachDeliveryFeePaidAmnt',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtEachDeliveryFeePaidAmnt','3000',runtext)

                elif gd == 10:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 조건부/선결제'
                    desktopWeb.idClick('rdoEachDeliveryFeeType3',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.idClear('txtEachDeliveryFeeConditionFreeAmnt1',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtEachDeliveryFeeConditionFreeAmnt1','1000',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.idClear('txtEachDeliveryFeeConditionFreeAmnt2',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtEachDeliveryFeeConditionFreeAmnt2','3000',runtext) 
                
                elif gd == 11:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 수량별차등/구매수량별'
                    desktopWeb.idClick('rdoEachDeliveryFeeType4',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[1]/span[1]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[1]/span[1]/input','2',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[1]/span[2]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[1]/span[2]/input','500',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[2]/span[2]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[2]/span[2]/input','1000',runtext)

                elif gd == 12:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 수량별차등/배송비구간'
                    desktopWeb.idClick('rdoEachDeliveryFeeType4',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[1]/span[1]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[1]/span[1]/input','2',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[1]/span[2]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[1]/span[2]/input','500',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[2]/span[2]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[2]/span[2]/input','1000',runtext)

            else:

                if ss == 0:

                    if gd == 14 :

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 무료배송 선택'
                        desktopWeb.idClick('TplDeliveryFree',runtext)

                    elif gd == 13:

                        runtext = '노출정보 > 배송정보 > 배송비 설정 > 유료배송 선택'
                        desktopWeb.idClick('TplDeliveryFee',runtext)

        elif check == 'p':
            
            deliveryCondition = dc
            if deliveryCondition == 1:
            # 무료, 유료/선결제, 유료/착불, 유료/착불&선결제, 조건부/착불&선결제, 조건부/선결제, 조건부/착불

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 선택'
                desktopWeb.idClick('rdoDeliveryFeeType1',runtext)
                
                if gd == 1:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 무료'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'무료 (664208)',runtext)

                elif gd == 2:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 유료/선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'유료/2,500원/선결제 선택 (664234)',runtext)

                elif gd == 3:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 유료/착불'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'유료/2,500원/착불 선택 (664136)',runtext)

                elif gd == 4:
                            
                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 유료/착불&선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'유료/5,000원/착불&선결제 선택 (664237)',runtext)

                elif gd == 5:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 조건부/착불&선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'조건부무료-50,000원 이상 무료/50,000원 미만 2500원/착불&선결제 선택 (664198)',runtext)

                elif gd == 6:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 조건부/선결제'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'조건부무료-50,000원 이상 무료/50,000원 미만 2500원/선결제 선택 (664224)',runtext)

                elif gd == 7:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 묶음 배송비 > 배송비 템플릿 선택 > 조건부/착불'
                    desktopWeb.idSelectby('selBundleDeliveryTemp',1, u'조건부무료-50,000원 이상 무료/50,000원 미만 3000원/착불 선택 (664273)',runtext)
            
            else:
                # 무료, 유료/선결제, 조건부/선결제, 수량별차등/구매수량별, 수량별차등/배송비구간

                runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 선택'
                desktopWeb.idClick('rdoDeliveryFeeType2',runtext)

                if gd == 8:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 무료'
                    desktopWeb.idClick('rdoEachDeliveryFeeType1',runtext)
                
                elif gd == 9:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 유료/선결제'
                    desktopWeb.idClick('rdoEachDeliveryFeeType2',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtEachDeliveryFeePaidAmnt','3000',runtext)

                elif gd == 10:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 조건부/선결제'
                    desktopWeb.idClick('rdoEachDeliveryFeeType3',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.idClear('txtEachDeliveryFeeConditionFreeAmnt1',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtEachDeliveryFeeConditionFreeAmnt1','1000',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.idClear('txtEachDeliveryFeeConditionFreeAmnt2',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtEachDeliveryFeeConditionFreeAmnt2','3000',runtext) 
                
                elif gd == 11:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 수량별차등/구매수량별'
                    desktopWeb.idClick('rdoEachDeliveryFeeType4',runtext)

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 수량별차등/구매수량별 > 구매수량별 반복추가 선택'
                    desktopWeb.idClick('rdoEachDeliveryFeeQTYEachGradeType3',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.idClear('txtRepeatBuyQTY',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtRepeatBuyQTY','2',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.idClear('txtRepeatDeliveryFee',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.idKey('txtRepeatDeliveryFee','500',runtext)
                    
                elif gd == 12:

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 수량별차등/배송비구간'
                    desktopWeb.idClick('rdoEachDeliveryFeeType4',runtext)

                    runtext = '노출정보 > 배송정보 > 배송비 설정 > 배송비 선택 > 상품별 배송비 > 배송비 선택 > 수량별차등/구매수량별 > 배송비 구간 직접 입력 선택'
                    desktopWeb.idClick('rdoEachDeliveryFeeQTYEachGradeType4',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[1]/span[1]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[1]/span[1]/input','2',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[1]/span[2]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[1]/span[2]/input','500',runtext)

                    runtext = '배송비 금액/조건 삭제'
                    desktopWeb.xpathClear('//*[@id="QTYList"]/li[2]/span[2]/input',runtext)

                    runtext = '배송비 금액/조건 기입'
                    desktopWeb.xpathKey('//*[@id="QTYList"]/li[2]/span[2]/input','1000',runtext)

    # 복수구매할인 확인
    def multiple_Purchase_Check(check,gd,discount):

        multiple_purchase_check = 0

        if check == 'n':

            if gd == 5:

                runtext = '복수구매할인 > 설정하기 버튼 선택'
                runtexttext = '복수구매할인 체크박스 체크 유무'
                y_n = desktopWeb.idSelected('chkGmkBuyerBenefitIsUsed',runtext,runtexttext)

                if y_n == 0:

                    runtext = '복수구매할인 > 복구수매할인 종류 확인'
                    runtexttext = '구매수량별 할인 설정'
                    visible = desktopWeb.idDisplayed('ddGmkBuyerBenefitS',runtext,runtexttext)

                    if visible == 0:

                        runtext = '복수구매할인 > 복수구매할인 추출'
                        x = desktopWeb.idReturnAttribute('SYIStep3_GmkBuyerBenefit_UnitValue','value',runtext)

                        if ',' in x:

                            x = x.replace(',','')

                        if int(discount) == int(x):

                            multiple_purchase_check = 0

                        elif int(discount) != int(x):

                            multiple_purchase_check = 1
                        
                    elif visible == 1:

                        multiple_purchase_check = 1

                elif y_n == 1:

                    multiple_purchase_check = 1
            
        elif check == 'p':

            if gd == 5:

                runtext = '복수구매할인 > 설정하기 버튼 선택'
                runtexttext = '복수구매할인 체크박스 체크 유무'
                y_n = desktopWeb.xpathSelected('//*[@id="divGmkBuyerBenefit"]/p/label[2]',runtext,runtexttext)

                if y_n == 0:

                    runtext = '복수구매할인 > 복수구매할인 추출'
                    x = desktopWeb.idReturnAttribute('SYIStep3_SellerDiscount_DiscountAmtGmkt|SYIStep3_SellerDiscount_DiscountAmt','value',runtext)

                    if ',' in x:

                        x = x.replace(',','')

                        if int(discount) == int(x):

                            multiple_purchase_check = 0

                        elif int(discount) != int(x):

                            multiple_purchase_check = 1

                elif y_n == 1:

                    multiple_purchase_check = 1
        
        return multiple_purchase_check

    # 복수구매할인
    def multiple_Purchase(check,gd,discount):

        if check == 'n':

            if gd == 5:

                runtext = '복수구매할인 > 설정하기 버튼 선택'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'
                y_n = desktopWeb.idSelected('chkGmkBuyerBenefitIsUsed',runtext,runtexttext)

                if y_n == 0:

                    pass
                
                elif y_n == 1:

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인버튼 선택'
                    desktopWeb.idClick('chkGmkBuyerBenefitIsUsed',runtext)

                today = datetime.today().strftime('%Y-%m-%d')   
                next_day = datetime.today() + timedelta(90)
                next_day = next_day.strftime('%Y-%m-%d')

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 구매수량별 할인 설정 선택'
                desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_Type',1,'구매수량별 할인 설정',runtext)
                time.sleep(1)
                
                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 적용기간 삭제'
                desktopWeb.xpathKey("//input[@id='SYIStep3_GmkBuyerBenefit_EndDate']",'clear',runtext)
                time.sleep(1)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 적용기간 기입'
                desktopWeb.xpathKey("//input[@id='SYIStep3_GmkBuyerBenefit_EndDate']",next_day,runtext)
                time.sleep(1)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 적용기간 기입'
                desktopWeb.xpathKey("//input[@id='SYIStep3_GmkBuyerBenefit_EndDate']",'enter',runtext)
                time.sleep(1)



                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 구매수량별 할인 설정 선택'
                desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_Type',1, u'구매수량별 할인 설정',runtext)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 구매수량 삭제'
                desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_ConditionValue','clear',runtext)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 구매수량 기입'
                desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_ConditionValue','2',runtext)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 개(수량)선택'
                desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_ConditionType',1,u'개(수량)',runtext)

                discount = int(discount)
                if discount > 10:

                    ranmdom = '1'

                else:

                    ranmdom = '2'

                if ranmdom == '1':

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 원 선택'
                    desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_Unit',1,u'원',runtext)

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 정액 할인율 삭제'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue','clear',runtext)

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 정액 할인율 기입'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue',discount,runtext)

                elif ranmdom == '2':

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > % 선택'
                    desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_Unit',1,u'%',runtext)

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 정율 할인율 삭제'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue','clear',runtext)

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 정율 할인율 기입'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue',discount,runtext)
            
            else:

                runtext = '복수구매할인 > 설정하기 버튼 선택'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'
                y_n = desktopWeb.idSelected('chkGmkBuyerBenefitIsUsed',runtext,runtexttext)
            
                if y_n == 0:

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인버튼 선택'
                    desktopWeb.idClick('chkGmkBuyerBenefitIsUsed',runtext)
                
                elif y_n == 1:

                    pass
        
        elif check == 'p':

            if gd == 5:

                runtext = '복수구매할인 > 설정하기 버튼 선택'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'
                y_n = desktopWeb.xpathSelected('//*[@id="divGmkBuyerBenefit"]/p/label[2]',runtext,runtexttext)
                

                if y_n == 0:

                    pass
                
                elif  y_n == 1:

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매 사용 버튼 선택'
                    desktopWeb.xpathClick('//*[@id="divGmkBuyerBenefit"]/p/label[2]',runtext)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 구매수량별 할인 설정 선택'
                desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_Type',1, u'구매수량별 할인 설정',runtext)

                runtext = '할인율 삭제'
                desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_ConditionValue','clear',runtext)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 구매수량 기입'
                desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_ConditionValue','2',runtext)

                runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 개(수량)선택'                                                                                                                                                                                                                                               
                desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_ConditionType',1,u'개(수량)',runtext)

                discount = int(discount)
                if discount > 10:

                    ranmdom = '1'

                else:

                    ranmdom = '2'

                if ranmdom == '1':

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 원 선택'
                    desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_Unit',1,u'원',runtext)

                    runtext = '할인율 삭제'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue','clear',runtext)

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 정액 할인율 기입'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue',discount,runtext)

                elif ranmdom == '2':

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > % 선택'
                    desktopWeb.idSelectby('SYIStep3_GmkBuyerBenefit_Unit',1,u'%',runtext)

                    runtext = '할인율 삭제'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue','clear',runtext)

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매할인 > 정율 할인율 기입'
                    desktopWeb.idKey('SYIStep3_GmkBuyerBenefit_UnitValue',discount,runtext)
            
            else:

                runtext = '복수구매할인 > 설정하기 버튼 선택'
                runtexttext = '판매자 부담할인 체크박스 체크 유무'
                y_n = desktopWeb.xpathSelected('//*[@id="divGmkBuyerBenefit"]/p/label[2]',runtext,runtexttext)
            
                if y_n == 0:

                    runtext = '고객혜택/광고 > 고객혜택서비스 > 복수구매 미사용 버튼 선택'
                    desktopWeb.xpathSelected('//*[@id="divGmkBuyerBenefit"]/p/label[1]',runtext)
                
                elif y_n == 1:

                    pass

    # BSD세일(1.0)
    def BSD(price):

        runtext = '경고창 제어'
        text = desktopWeb.alerClose(runtext)

        if text == '인하':
            
            price = str(price)
            price = price.replace(',','')
            price = int(price)
            a = price * 0.9
            b = a % 10

            price = a - b

            #BSD 상품 가격 인하
            runtext = '기존 상품가격 삭제'
            desktopWeb.idClear('txtGoodsPrice',runtext)

            runtext = '상품가격 새 기입'
            desktopWeb.idKey('txtGoodsPrice',price,runtext)

            runtext = '가격 변경 실수 방지 노출 확인'
            desktopWeb.xpathClick('//*[@id="sectionSellingPeriod"]/th/div',runtext)
            time.sleep(2)
            
            runtext = '가격 변경 실수 방지 유무 확인'
            runtexttext = '가격변경 실수 방지 노출'
            price_Fluctuations = desktopWeb.idDisplayed('divGoodsPriceConfirm',runtext,runtexttext)

            if price_Fluctuations == 0: #큰 폭의 가격변동일때

                runtext = '가격'
                res = desktopWeb.idReturnText('divGoodsPriceChnagedHangul',runtext)

                runtext = '실수 방지 가격 삭제'
                desktopWeb.idClear('txtGoodsPriceChangedHangulConfirm',runtext)

                runtext = '실수 방지 가격 기입'
                desktopWeb.idKey('txtGoodsPriceChangedHangulConfirm',res,runtext)
            
            else:

                pass

            runtext = '상품수정 > 수정하기 버튼 선택'
            desktopWeb.idClick('SaveItem',runtext)
            time.sleep(3)
        
    # ESM 1.0,2.0 통합 확인
    def ESM_check(self,goods_Number,goods_Price,goods_deliveryCondition,deliveryCondition,goods_discount,discount,goods_Name):

        xxx = 0
        price_check = 0
        seller_discount_check = 0
        multiple_purchase_check = 0
        delivery_Check = 0
        ESM_controll.login(self,goods_Name)
        time.sleep(6)

        ESM_controll.ESM_HOME(self)

        check = ESM_controll.Goods_manage(self,goods_Number)

        if check == 'n':

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리2.0 선택'
                desktopWeb.idKey('tTDM396','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)
            
            # 상품수정 2.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)
            
            runtext = '상품수정 2.0 확인'
            wait = desktopWeb.xpathWait('//*[@class="item"]/th[1]/div/span|//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[1]/th/div/span',runtext)

            if wait != 0:

                runtext = '페이지 새로고침'
                desktopWeb.webrefresh(runtext)

                runtext = 'Default 창 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'ESM 홈 > 팝업창 제어'
                desktopWeb.popupClose(runtext)

                runtext = 'Layer 팝업'
                runtexttext = 'ESM 홈 > Layer 팝업 제어'
                desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품번호 기입' 
                desktopWeb.xpathKey('//*[@id="txtGoodsId"]|//*[@class="textarea"]/textarea', goods_Number, runtext)
                time.sleep(1)

                runtext = '상품관리2.0 > 검색하기 버튼 선택'
                desktopWeb.xpathClick('//*[@id="imgItemsSearch"]',runtext)
                time.sleep(3)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)

                runtext = '첫번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '두번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '원래 Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = 'Layer 경고문 제어'
                runtexttext = 'Layer 경고문 제어'
                desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            runtext = '스마일배송 판별'
            runtexttext = '스마일 배송'
            smileShipping = desktopWeb.xpathDisplayed('//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[3]/td/div/div/div/div/span',runtext,runtexttext)
            
            if smileShipping == 1:
                ESM_controll.Sales_period(check)

            price_check = ESM_controll.Price_Check(check,goods_Price)

            seller_discount_check = ESM_controll.Seller_Discount_Check(check,goods_discount,discount)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)

            # 노출정보
            delivery_Check = ESM_controll.delivery_Check(check,smileShipping,goods_deliveryCondition,deliveryCondition)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)
            time.sleep(3)

            # 추가정보
            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[3]/div/ol/li[4]',runtext)
            time.sleep(3)

            # 고객혜택/광고
            multiple_purchase_check = ESM_controll.multiple_Purchase_Check(check,goods_discount,discount)

        elif check == 'p':

            smileShipping = 1

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리1.0 선택'
                desktopWeb.idKey('tTDM100','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                
                time.sleep(10)

            # 상품수정 1.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)
            
            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            runtext = '상품수정 > 전체 상품정보 수정 선택'
            desktopWeb.xpathClick('//*[@id="modify_type"]/li[2]',runtext)

            ESM_controll.Sales_period(check)

            price_check = ESM_controll.Price_Check(check,goods_Price)

            delivery_Check = ESM_controll.delivery(check,0,goods_deliveryCondition, deliveryCondition)

            seller_discount_check = ESM_controll.Seller_Discount_Check(check,goods_discount,discount)

            multiple_purchase_check = ESM_controll.multiple_Purchase_Check(check,goods_discount,discount)

        elif check == 'nono':

            xxx = 1

        common.desktopWebClose()

        return price_check, seller_discount_check, multiple_purchase_check, delivery_Check, xxx

    # ESM 1.0,2.0 통합 확인
    def ESM_check2(self,goods_Number,goods_Price,goods_deliveryCondition,deliveryCondition,goods_discount,discount):

        xxx = 0 
        price_check = 0
        seller_discount_check = 0
        multiple_purchase_check = 0
        delivery_Check = 0
        check = ESM_controll.Goods_manage(self,goods_Number)

        if check == 'n':

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리2.0 선택'
                desktopWeb.idKey('tTDM396','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)
            
            # 상품수정 2.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)
            
            runtext = '상품수정 2.0 확인'
            wait = desktopWeb.xpathWait('//*[@class="item"]/th[1]/div/span|//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[1]/th/div/span',runtext)

            if wait != 0:

                runtext = '페이지 새로고침'
                desktopWeb.webrefresh(runtext)

                runtext = 'Default 창 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'ESM 홈 > 팝업창 제어'
                desktopWeb.popupClose(runtext)

                runtext = 'Layer 팝업'
                runtexttext = 'ESM 홈 > Layer 팝업 제어'
                desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품번호 기입' 
                desktopWeb.xpathKey('//*[@id="txtGoodsId"]|//*[@class="textarea"]/textarea', goods_Number, runtext)
                time.sleep(1)

                runtext = '상품관리2.0 > 검색하기 버튼 선택'
                desktopWeb.xpathClick('//*[@id="imgItemsSearch"]',runtext)
                time.sleep(3)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)

                runtext = '첫번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '두번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '원래 Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = 'Layer 경고문 제어'
                runtexttext = 'Layer 경고문 제어'
                desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            runtext = '스마일배송 판별'
            runtexttext = '스마일 배송'
            smileShipping = desktopWeb.xpathDisplayed('//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[3]/td/div/div/div/div/span',runtext,runtexttext)
            
            if smileShipping == 1:
                ESM_controll.Sales_period(check)

            price_check = ESM_controll.Price_Check(check,goods_Price)

            seller_discount_check = ESM_controll.Seller_Discount_Check(check,goods_discount,discount)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)

            # 노출정보
            delivery_Check = ESM_controll.delivery_Check(check,smileShipping,goods_deliveryCondition,deliveryCondition)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)
            time.sleep(3)

            # 추가정보
            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[3]/div/ol/li[4]',runtext)
            time.sleep(3)

            # 고객혜택/광고
            multiple_purchase_check = ESM_controll.multiple_Purchase_Check(check,goods_discount,discount)

        elif check == 'p':

            smileShipping = 1

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리1.0 선택'
                desktopWeb.idKey('tTDM100','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                
                time.sleep(10)

            # 상품수정 1.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)
            
            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            runtext = '상품수정 > 전체 상품정보 수정 선택'
            desktopWeb.xpathClick('//*[@id="modify_type"]/li[2]',runtext)

            ESM_controll.Sales_period(check)

            price_check = ESM_controll.Price_Check(check,goods_Price)

            delivery_Check = ESM_controll.delivery(check,0,goods_deliveryCondition, deliveryCondition)

            seller_discount_check = ESM_controll.Seller_Discount_Check(check,goods_discount,discount)

            multiple_purchase_check = ESM_controll.multiple_Purchase_Check(check,goods_discount,discount)

        elif check == 'nono':

            xxx = 1

        common.desktopWebClose()

        return price_check, seller_discount_check, multiple_purchase_check, delivery_Check, xxx

    # ESM 수정 1.0,2.0 통합 수정
    def ESM_modify(self,goods_Number,goods_Price,goods_deliveryCondition,deliveryCondition,goods_discount,discount,goods_Name):
        
        xxx = 0
        ESM_controll.login(self,goods_Name)
        time.sleep(6)

        ESM_controll.ESM_HOME(self)

        check = ESM_controll.Goods_manage(self,goods_Number)

        if check == 'n':

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Default 창 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리2.0 선택'
                desktopWeb.idKey('tTDM396','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼'
                runtexttext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClickSkip('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)
            
            # 상품수정 2.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)
            
            runtext = '상품수정 2.0 확인'
            wait = desktopWeb.xpathWait('//*[@class="item"]/th[1]/div/span|//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[1]/th/div/span',runtext)

            if wait != 0:

                runtext = '페이지 새로고침'
                desktopWeb.webrefresh(runtext)

                runtext = 'Default 창 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'ESM 홈 > 팝업창 제어'
                desktopWeb.popupClose(runtext)

                runtext = 'Layer 팝업'
                runtexttext = 'ESM 홈 > Layer 팝업 제어'
                desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품번호 기입' 
                desktopWeb.xpathKey('//*[@id="txtGoodsId"]|//*[@class="textarea"]/textarea', goods_Number, runtext)
                time.sleep(1)

                runtext = '상품관리2.0 > 검색하기 버튼 선택'
                desktopWeb.xpathClick('//*[@id="imgItemsSearch"]',runtext)
                time.sleep(3)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)

                runtext = '첫번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '두번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '원래 Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = 'Layer 경고문 제어'
                runtexttext = 'Layer 경고문 제어'
                desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            if goods_Name == 23 or goods_Name == 24:

                smileShipping = 0

            else:

                runtext = '스마일배송 판별'
                runtexttext = '스마일 배송'
                smileShipping = desktopWeb.xpathDisplayed('//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[3]/td/div/div/div/div/span',runtext,runtexttext)
            
            runtext = 'ESM 상품 식별코드 확인'
            runtexttext = 'ESM 상품 식별코드'
            cheche = desktopWeb.idDisplayed('sectionEPIN',runtext,runtexttext)

            if cheche == 0:
                
                runtext = 'ESM 상품 식별코드 등록 확인'
                runtexttext = 'ESM 상품 식별코드 1'
                x = desktopWeb.idDisplayed('divEPINDetail',runtext,runtexttext)

                runtext = 'ESM 상품 식별코드 등록 확인'
                runtexttext = 'ESM 상품 식별코드 2'
                y = desktopWeb.idDisplayed('epinCreateRequestNotice',runtext,runtexttext)

                runtext = 'ESM 상품 식별코드 등록 확인'
                runtexttext = 'ESM 상품 식별코드 3'
                z = desktopWeb.idDisplayed('epinCreateRequestInfo',runtext,runtexttext)

                if x == 0 or y == 0 or z == 0:

                    pass

                else:

                    runtext = 'ESM 카테고리 추출'
                    name = desktopWeb.xpathReturnText('//*[@class="market market--esm cols"]/div/div[1]/p/span',runtext)

                    name = name.strip()
                    
                    runtext = 'ESM 상품식별코드 기입'
                    desktopWeb.idKey('txtEPINSearchKeyword',name,runtext)
                    time.sleep(2)

                    runtext = 'ESM 상품식별코드 삭제'
                    desktopWeb.idKey('txtEPINSearchKeyword','clear',runtext)
                    desktopWeb.idClick('txtEPINSearchKeyword',runtext)
                    time.sleep(3)

                    runtext = '돋보기 위치 파악'
                    coordinate = desktopWeb.imageCoordinate(ESM_path+'search.png',runtext,99/100,1/2,0.8)

                    runtext = 'ESM 상품식별코드 기입'
                    desktopWeb.idKey('txtEPINSearchKeyword',name,runtext)
                    time.sleep(2)

                    runtext = '돋보기 선택'
                    desktopWeb.webPyautoguiClick(coordinate,runtext)
                    time.sleep(10)

                    runtext = '등록하기 버튼 선택'
                    desktopWeb.xpathKey('//*[@id="epinSearchList"]/li[1]/div/button','enter',runtext)

            else:
                pass

            if smileShipping == 1:
                ESM_controll.Sales_period(check)

            ESM_controll.Price_Change(check,goods_Price)

            ESM_controll.Seller_Discount(check,goods_discount,discount)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)

            # 노출정보
            ESM_controll.delivery(check,smileShipping,goods_deliveryCondition,deliveryCondition)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)
            time.sleep(3)

            # 추가정보
            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[3]/div/ol/li[4]',runtext)
            time.sleep(3)

            # 고객혜택/광고
            ESM_controll.multiple_Purchase(check,goods_discount,discount)

            runtext = '고객혜택/광고 > 수정하기 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[3]/div/div/a',runtext)
            time.sleep(3)

        elif check == 'p':

            smileShipping = 1

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리1.0 선택'
                desktopWeb.idKey('tTDM100','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                
                time.sleep(10)

            # 상품수정 1.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)
            
            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            runtext = '상품수정 > 전체 상품정보 수정 선택'
            desktopWeb.xpathClick('//*[@id="modify_type"]/li[2]',runtext)

            ESM_controll.Sales_period(check)

            before_Price = ESM_controll.Price_Change(check,goods_Price)

            runtext = '상품관리 > 배송정보 설정 > 배송비 설정 > 출하지 선택'
            desktopWeb.idSelectby('selShipmentPlaceNo',1,u'STA TEST11',runtext)
            time.sleep(3)

            ESM_controll.delivery(check,0,goods_deliveryCondition, deliveryCondition)

            runtext = '상품관리 > 원산지'
            origin = desktopWeb.xpathReturnAttribute('//*[@id="sectionGoodsOrigin"]/th/div','class',runtext)

            if origin == 'th1 must':

                runtext = '상품관리 > 원산지 > 각 상품별 원산지는 상세설명 참조 선택'
                desktopWeb.idClick('rdoOriginProductTypeInside',runtext)

            else:

                pass

            ESM_controll.Seller_Discount(check,goods_discount,discount)

            ESM_controll.multiple_Purchase(check,goods_discount,discount)

            runtext = '상품수정 > 수정하기 버튼 선택'
            desktopWeb.idClick('SaveItem',runtext)
            time.sleep(3)

            ESM_controll.BSD(before_Price)

        elif check == 'nono':

            xxx = 1

        if check == 'n' or check == 'p':

            runtext = 'ESM 상품정보확인 팝업창 확인'
            popupnumber = desktopWeb.popupCheck(runtext)

            popupnumber = int(popupnumber)
            if popupnumber == 2:

                runtext = 'ESM 상품정보확인 팝업창 제어'
                desktopWeb.popupControl(1,runtext)

                runtext = '상품정보확인 > 이미지 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lbConfirmForGoodsImage','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 이미지 확인 버튼 선택'
                    desktopWeb.idClick('lbConfirmForGoodsImage',runtext)
                else:

                    pass
                time.sleep(1)
                
                runtext = '상품정보확인 > 상품몀 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lblConfirmForGoodsName','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 상품명 확인 버튼 선택'
                    desktopWeb.idClick('lblConfirmForGoodsName',runtext)
                else:

                    pass
                time.sleep(1)

                runtext = '상품정보확인 > 판매자부담할인 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lblConfirmForSellerDiscount','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 상품명 확인 버튼 선택'
                    desktopWeb.idClick('lblConfirmForSellerDiscount',runtext)
                else:

                    pass
                time.sleep(1)

                runtext = '상품정보확인 > 판매가격 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lblConfirmForGoodsPrice','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 판매가격 확인 버튼 선택'
                    desktopWeb.idClick('lblConfirmForGoodsPrice',runtext)
                else:

                    pass
                time.sleep(1)

                if smileShipping == 0:

                    runtext = '상품정보확인 > SKU정보 확인 버튼 체크유무 확인'
                    y_n =desktopWeb.idReturnAttribute('lbConfirmForSKU','class',runtext)

                    if y_n == 'btn-confirm':

                        runtext = '상품정보확인 > 판매가격 확인 버튼 선택'
                        desktopWeb.idClick('lbConfirmForSKU',runtext)
                    else:

                        pass
                    time.sleep(1)

                    runtext = '상품정보확인 > 아래로 스크롤'
                    desktopWeb.idKey('lbConfirmForSKU','tab',runtext)
                    time.sleep(1)

                runtext = '상품정보확인 > 아래로 스크롤'
                desktopWeb.jsScrollo_dwon(runtext)
                time.sleep(1)

                runtext = '상품정보확인 > 최종확인 버튼 선택'
                desktopWeb.imageClick(ESM_path+'last_confirm.png',runtext)
                time.sleep(1)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = 'ESM 상품등록 회귀'
            desktopWeb.popupOrginal(runtext)
            time.sleep(5)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = '스크린 샷'
            desktopWeb.weballScreenshot(goods_Number+'ESM',runtext)

            runtext = '상품 수정 확인'
            modify_check = desktopWeb.xpathCheck('//*[@class="product_complete_group"]/h4/img',runtext)

            if modify_check == 'p':

                xxx = 111

        common.desktopWebClose()

        return xxx
    
    # ESM 수정 1.0,2.0 통합 수정
    def ESM_modify2(self,goods_Number,goods_Price,goods_deliveryCondition,deliveryCondition,goods_discount,discount,goods_Name):

        xxx = 0
        check = ESM_controll.Goods_manage(self,goods_Number)

        if check == 'n':

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Default 창 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리2.0 선택'
                desktopWeb.idKey('tTDM396','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼'
                runtexttext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClickSkip('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)
            
            # 상품수정 2.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)
            
            runtext = '상품수정 2.0 확인'
            wait = desktopWeb.xpathWait('//*[@class="item"]/th[1]/div/span|//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[1]/th/div/span',runtext)

            if wait != 0:

                runtext = '페이지 새로고침'
                desktopWeb.webrefresh(runtext)

                runtext = 'Default 창 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'ESM 홈 > 팝업창 제어'
                desktopWeb.popupClose(runtext)

                runtext = 'Layer 팝업'
                runtexttext = 'ESM 홈 > Layer 팝업 제어'
                desktopWeb.xpathClickSkip('//*[@id="popFooter"]/a/img',runtext,runtexttext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리2.0 > 상품번호 기입' 
                desktopWeb.xpathKey('//*[@id="txtGoodsId"]|//*[@class="textarea"]/textarea', goods_Number, runtext)
                time.sleep(1)

                runtext = '상품관리2.0 > 검색하기 버튼 선택'
                desktopWeb.xpathClick('//*[@id="imgItemsSearch"]',runtext)
                time.sleep(3)

                runtext = '상품관리2.0 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@id="gridview-1012"]/table/tbody/tr[2]/td[6]/div/a/img|//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                time.sleep(10)

                runtext = '첫번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '두번째 경고창 제어'
                desktopWeb.alerClose(runtext)

                runtext = '원래 Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = 'Layer 경고문 제어'
                runtexttext = 'Layer 경고문 제어'
                desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            if goods_Name == 23 or goods_Name == 24:

                smileShipping = 0

            else:

                runtext = '스마일배송 판별'
                runtexttext = '스마일 배송'
                smileShipping = desktopWeb.xpathDisplayed('//*[@id="SingleGoodsApp"]/div[1]/div/table/tbody/tr[3]/td/div/div/div/div/span',runtext,runtexttext)
            
            runtext = 'ESM 상품 식별코드 확인'
            runtexttext = 'ESM 상품 식별코드'
            cheche = desktopWeb.idDisplayed('sectionEPIN',runtext,runtexttext)

            if cheche == 0:
                
                runtext = 'ESM 상품 식별코드 등록 확인'
                runtexttext = 'ESM 상품 식별코드 1'
                x = desktopWeb.idDisplayed('divEPINDetail',runtext,runtexttext)

                runtext = 'ESM 상품 식별코드 등록 확인'
                runtexttext = 'ESM 상품 식별코드 2'
                y = desktopWeb.idDisplayed('epinCreateRequestNotice',runtext,runtexttext)

                runtext = 'ESM 상품 식별코드 등록 확인'
                runtexttext = 'ESM 상품 식별코드 3'
                z = desktopWeb.idDisplayed('epinCreateRequestInfo',runtext,runtexttext)

                if x == 0 or y == 0 or z == 0:

                    pass

                else:

                    runtext = 'ESM 카테고리 추출'
                    name = desktopWeb.xpathReturnText('//*[@class="market market--esm cols"]/div/div[1]/p/span',runtext)

                    name = name.strip()
                    
                    runtext = 'ESM 상품식별코드 기입'
                    desktopWeb.idKey('txtEPINSearchKeyword',name,runtext)
                    time.sleep(2)

                    runtext = 'ESM 상품식별코드 삭제'
                    desktopWeb.idKey('txtEPINSearchKeyword','clear',runtext)
                    desktopWeb.idClick('txtEPINSearchKeyword',runtext)
                    time.sleep(3)

                    runtext = '돋보기 위치 파악'
                    coordinate = desktopWeb.imageCoordinate(ESM_path+'search.png',runtext,99/100,1/2,0.8)

                    runtext = 'ESM 상품식별코드 기입'
                    desktopWeb.idKey('txtEPINSearchKeyword',name,runtext)
                    time.sleep(2)

                    runtext = '돋보기 선택'
                    desktopWeb.webPyautoguiClick(coordinate,runtext)
                    time.sleep(10)

                    runtext = '등록하기 버튼 선택'
                    desktopWeb.xpathKey('//*[@id="epinSearchList"]/li[1]/div/button','enter',runtext)

            else:
                pass

            if smileShipping == 1:
                ESM_controll.Sales_period(check)

            ESM_controll.Price_Change(check,goods_Price)

            ESM_controll.Seller_Discount(check,goods_discount,discount)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)

            # 노출정보
            ESM_controll.delivery(check,smileShipping,goods_deliveryCondition,deliveryCondition)

            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[5]/a[3]',runtext)
            time.sleep(3)

            # 추가정보
            runtext = '다음 단계로 이동 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[3]/div/ol/li[4]',runtext)
            time.sleep(3)

            # 고객혜택/광고
            ESM_controll.multiple_Purchase(check,goods_discount,discount)

            runtext = '고객혜택/광고 > 수정하기 버튼 선택'
            desktopWeb.xpathClick('//*[@id="contents"]/div[3]/div/div/a',runtext)
            time.sleep(3)

        elif check == 'p':

            smileShipping = 1

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)
            time.sleep(1)

            runtext = '오류'
            a = desktopWeb.xpathCheck('//*[@class="etc_notice_wrap"]/div/strong/img',runtext)

            if a == 'p':

                pass

            elif a == 'n':

                runtext = 'Frame 전환'
                desktopWeb.frameSwitchOrginal(runtext)

                runtext = '상품관리1.0 선택'
                desktopWeb.idKey('tTDM100','enter',runtext)
                time.sleep(2)

                runtext = 'Frame 전환'
                desktopWeb.frameSwitch(runtext)

                runtext = '상품관리 > 상품관리 > 상품 수정 버튼 선택'
                desktopWeb.xpathClick('//*[@class=" x-grid-cell x-grid-cell-modifyGoods   "]/div/a/img',runtext)
                
                time.sleep(10)

            # 상품수정 1.0 
            runtext = '첫번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '두번째 경고창 제어'
            desktopWeb.alerClose(runtext)

            runtext = '원래 Frame 전환'
            desktopWeb.frameSwitchOrginal(runtext)
            
            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = 'Layer 경고문 제어'
            runtexttext = 'Layer 경고문 제어'
            desktopWeb.xpathClickSkip('//*[@id="showBlockBSD"]/div/div/button',runtext, runtexttext)

            runtext = '상품수정 > 전체 상품정보 수정 선택'
            desktopWeb.xpathClick('//*[@id="modify_type"]/li[2]',runtext)

            ESM_controll.Sales_period(check)

            before_Price = ESM_controll.Price_Change(check,goods_Price)

            runtext = '상품관리 > 배송정보 설정 > 배송비 설정 > 출하지 선택'
            desktopWeb.idSelectby('selShipmentPlaceNo',1,u'STA TEST11',runtext)
            time.sleep(3)

            ESM_controll.delivery(check,0,goods_deliveryCondition, deliveryCondition)

            runtext = '상품관리 > 원산지'
            origin = desktopWeb.xpathReturnAttribute('//*[@id="sectionGoodsOrigin"]/th/div','class',runtext)

            if origin == 'th1 must':

                runtext = '상품관리 > 원산지 > 각 상품별 원산지는 상세설명 참조 선택'
                desktopWeb.idClick('rdoOriginProductTypeInside',runtext)

            else:

                pass

            ESM_controll.Seller_Discount(check,goods_discount,discount)

            ESM_controll.multiple_Purchase(check,goods_discount,discount)

            runtext = '상품수정 > 수정하기 버튼 선택'
            desktopWeb.idClick('SaveItem',runtext)
            time.sleep(3)

            ESM_controll.BSD(before_Price)

        elif check == 'nono':

            xxx = 1

        if check == 'n' or check == 'p':

            runtext = 'ESM 상품정보확인 팝업창 확인'
            popupnumber = desktopWeb.popupCheck(runtext)

            popupnumber = int(popupnumber)
            if popupnumber == 2:

                runtext = 'ESM 상품정보확인 팝업창 제어'
                desktopWeb.popupControl(1,runtext)

                runtext = '상품정보확인 > 이미지 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lbConfirmForGoodsImage','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 이미지 확인 버튼 선택'
                    desktopWeb.idClick('lbConfirmForGoodsImage',runtext)
                else:

                    pass
                time.sleep(1)
                
                runtext = '상품정보확인 > 상품몀 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lblConfirmForGoodsName','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 상품명 확인 버튼 선택'
                    desktopWeb.idClick('lblConfirmForGoodsName',runtext)
                else:

                    pass
                time.sleep(1)

                runtext = '상품정보확인 > 판매자부담할인 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lblConfirmForSellerDiscount','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 상품명 확인 버튼 선택'
                    desktopWeb.idClick('lblConfirmForSellerDiscount',runtext)
                else:

                    pass
                time.sleep(1)

                runtext = '상품정보확인 > 판매가격 확인 버튼 체크유무 확인'
                y_n =desktopWeb.idReturnAttribute('lblConfirmForGoodsPrice','class',runtext)

                if y_n == 'btn-confirm':

                    runtext = '상품정보확인 > 판매가격 확인 버튼 선택'
                    desktopWeb.idClick('lblConfirmForGoodsPrice',runtext)
                else:

                    pass
                time.sleep(1)

                if smileShipping == 0:

                    runtext = '상품정보확인 > SKU정보 확인 버튼 체크유무 확인'
                    y_n =desktopWeb.idReturnAttribute('lbConfirmForSKU','class',runtext)

                    if y_n == 'btn-confirm':

                        runtext = '상품정보확인 > 판매가격 확인 버튼 선택'
                        desktopWeb.idClick('lbConfirmForSKU',runtext)
                    else:

                        pass
                    time.sleep(1)

                    runtext = '상품정보확인 > 아래로 스크롤'
                    desktopWeb.idKey('lbConfirmForSKU','tab',runtext)
                    time.sleep(1)

                runtext = '상품정보확인 > 아래로 스크롤'
                desktopWeb.jsScrollo_dwon(runtext)
                time.sleep(1)

                runtext = '상품정보확인 > 최종확인 버튼 선택'
                desktopWeb.imageClick(ESM_path+'last_confirm.png',runtext)
                time.sleep(1)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = '경고창 제어'
            desktopWeb.imageClick(ESM_path+'confirm.png',runtext)

            runtext = 'ESM 상품등록 회귀'
            desktopWeb.popupOrginal(runtext)
            time.sleep(5)

            runtext = 'Frame 전환'
            desktopWeb.frameSwitch(runtext)

            runtext = '스크린 샷'
            desktopWeb.weballScreenshot(goods_Number+'ESM',runtext)

            runtext = '상품 수정 확인'
            modify_check = desktopWeb.xpathCheck('//*[@class="product_complete_group"]/h4/img',runtext)

            if modify_check == 'p':

                xxx = 111

        common.desktopWebClose()

        return xxx