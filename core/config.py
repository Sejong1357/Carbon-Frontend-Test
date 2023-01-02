# -*- coding: utf-8 -*-
import sys
import os
import platform


allpath = os.path.abspath(__file__)
configpath = os.path.dirname(allpath)
sys.path.append(configpath)

from package import *

version = "1.000"
os_version = platform.platform()
chromecurrent = chromedriver_autoinstaller.get_chrome_version()  #크롬드라이버 버전 확인
chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
print('현재 Chromedriver version: ',chromecurrent)

# path =  allpath.replace('\core\con')
corepath = os.path.dirname(allpath)
path = os.path.dirname(corepath)
newchrome=path+'/'+chrome_ver
browserpath=path+'/webdriver/'

try:
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(f'./webdriver/chromedriver.exe'),options=chrome_options)
    driver.close()
    print('최신버전 업데이트 불필요')   
except:
    print('구버전 업데이트 진행')
    chromedriver_autoinstaller.install(True)
    print('업데이트 완료')

    shutil.move(newchrome+'/chromedriver.exe', browserpath+'chromedriver.exe')
    
    if os.path.exists(newchrome):
        os.rmdir(newchrome)

    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(f'./webdriver/chromedriver.exe'),options=chrome_options)
    driver.implicitly_wait(10)
    print('Chromedriver 정상 확인')
    print('END')

browser_version = chromedriver_autoinstaller.get_chrome_version()

###################################################################
###################################################################
###################################################################

# Slack Bot 환경 셋팅
my_slack = ''  # 토큰 값 입력ß
Slack1 = ''  # 구동 로그 채널 ID
Slack2 = ''  # 오류 로그 채널 ID
AutomationName = '[TEST] '

# 테스트 시나리오
txt1 = '-\t시나리오 상세 1'
txt2 = '-\t시나리오 상세 2'
txt3 = '-\t시나리오 상세 3'
txt4 = '-\t시나리오 상세 4'
tm1 = " *2. Test Scenario*`" + "``" + txt1 + "\n" + txt2 + "\n" + txt3 + "\n" + txt4 + "\n""```"

# 시스템 정보
tm2 = " *2. Automation System Info*`" + "``OS:\t" + os_version + "\nBrowser:\t" + browser_version + " ```"

# Appium 환경 셋팅
desired_caps = desired_caps = {
    "platformName": "Android",
    "platformVersion": "10.0",
    "deviceName": "GalaxyS10",
    "udid": "{}",
    "noReset": "false",
    "unicodeKeyboard": 'true',
    "resetKeyboard": "true",
    "appPackage": "{}",
    "appActivity": "{}",
    "app": "",
    "automationName": "UiAutomator2",
    'unicodeKeyboard': 'true'
}
