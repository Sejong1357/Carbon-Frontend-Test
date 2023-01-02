# -*- coding: utf-8 -*-

# 내부 구성 파일 불러오기
from config import *
from core.package import *
from core.testrail_api import APIClient

# PATH List
allpath= os.path.abspath(__file__)
corepath= os.path.dirname(allpath)
scriptpath = corepath.replace('\\core','')
imgpath= scriptpath+'\\image\\'
jsonpath= scriptpath+'\\json\\'
filepath= scriptpath+'\\file\\'

# timesleep
idsleep=5
xpathsleep=5
linktextsleep=5
classname = 5
tagname = 5
csssectorsleep = 5
webcommonsleep=5




###################################################################################
# Description : 공통 자동화하기 위한 Class
###################################################################################

class common:

    # 외부파일 위치 찾기
    def findfile(name, path,runtext):
        try:
            for dirpath, dirname, filename in os.walk(path):
                if name in filename:
                    print('file find Success ', '#', runtext)
                    return os.path.join(dirpath, name)
                
        except:
            print('file find Error ', '#', runtext)

    #외부파일 실행
    def fileRun(path,runtext): #외부파일 경로 기입
        try:
            file = os.path.abspath(path)
            os.startfile(file)
            print('file Run Success ', '#', runtext)
            time.sleep(3)
        except:
            print('file Run Error ', '#', runtext)

    #외부파일 실행
    def filerunRun(path,runtext): #외부파일 경로 기입
        try:
            os.system(path)
            print('file Run Success ', '#', runtext)
            time.sleep(3)
        except:
            print('file Run Error ', '#', runtext)



    #외부파일 종료
    def file_exit(file_name, runtext): #외부파일 이름 기입 확장자까지 기입(외부실행 파일일 경우 **.exe 로 기입)
        try:
            os.system('taskkill /f /im '+file_name)
            print('file exit Success', '#', runtext)
        except:
            print('file exit Error', '#', runtext)

    #WebError일 경우 강제 종료
    def desktopWebError():
        driver.quit()
        exit()

    #Web 종료
    def desktopWebClose():
        driver.close()
    
    #AppError일 경우 강제 종료
    def desktopAppError(): 
        exit()

    # 키보드 컨트롤 사용하고자 하는 키값 기입(str형) ex) enter 사용하고자 할 시, enter 기입
    # 반드시 키보드에 있는 영문타 입력할것 ex) control 키의 경우 키보드에 써져 있는 값 ctrl로 기입
    def KeyboardPress(key, runtext):
        for i in list(range(10)):
            try:
                pyautogui.press(key)
                print('success ', '#', runtext)
                time.sleep(1)
                return True
            except Exception as e:
                print('Error ', '#', runtext)
                print(e)
    
    # 화면 스크롤 원하는 스크롤 값 기입
    # 하단 스크롤 시 - 상단 스크롤 시 + 값 기입(양수 값일 경우 +무시 가능)
    def Scroll(number, runtext):
        for i in list(range(10)):
            try:
                pyautogui.scroll(number)
                print('success ', '#', runtext)
                time.sleep(1)
                return True
            except Exception as e:
                print('Error ', '#', runtext)
                print(e)
    

###################################################################################
# Description : PC Web Browser를 자동화하기 위한 Class
###################################################################################

class desktopWeb:

    #모든 Key 값은 default str형 주의 할 것

    def browserRun(browserName, path, runtext): # Browser 명 / 해당 Browser의 경로 / 동선 구간 명칭 등을 입력
        global driver
        for i in list(range(10)):
            try:
                if browserName == 'Chrome': # Browser명이 Chrome인 경우
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
                    driver = webdriver.Chrome(path, options=chrome_options)
                    print("#",browserName,runtext)
                    return driver
                elif browserName == 'IE': # Browser명이 IE인 경우
                    ie_options = Options()
                    ie_options.ignore_protected_mode_settings = True
                    ie_options.ignore_zoom_level = True
                    ie_options.require_window_focus = True
                    driver = webdriver.Ie(service=Service(path), options=ie_options)
                    print("#", browserName, runtext)
                    return driver
                else: # Browser명이 지원하지 않는 브라우저인 경우
                    print("Not Support Browser")
                    exit() 
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                exit()

    def noimage_browserRun(browserName, path, runtext): # Browser 명 / 해당 Browser의 경로 / 동선 구간 명칭 등을 입력
        global driver
        for i in list(range(10)):
            try:
                if browserName == 'Chrome': # Browser명이 Chrome인 경우
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
                    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
                    driver = webdriver.Chrome(path, options=chrome_options)
                    print("#",browserName,runtext)
                    return driver
                elif browserName == 'IE': # Browser명이 IE인 경우
                    ie_options = webdriver.IeOptions()
                    driver = webdriver.Ie(path, options=ie_options)
                    print("#", browserName, runtext)
                    return driver
                else: # Browser명이 지원하지 않는 브라우저인 경우
                    print("Not Support Browser")
                    exit() 
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                exit()

    def webaddressConnect(webAddress, runtext): # 접속할 타겟 URL 입력
        for i in list(range(10)):
            try:
                driver.get(webAddress) # 해당 URL 연결
                driver.maximize_window() # 창 최대화
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                driver.quit()
                exit()
    
    def webaddressadditionalConnect(webAddress, runtext): # 접속할 타겟 URL 입력

        for i in list(range(10)):
            try:
                driver.execute_script("window.open("+webAddress+");")
                tabs = driver.window_handles
                driver.switch_to.window(tabs[1])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                driver.quit()
                exit()
    
    def webrefresh(runtext):

        try:

            driver.refresh()
            print('#',runtext)
        
        except:

            print("Script Execution Error ", "#", runtext)
            exit()

    #Xpath
    def xpathCheck(xpath, runtext): # 해당 XPATH 값 유무 확인

        try:
            driver.find_element(By.XPATH,xpath)
            print("# "+runtext+ " Visible")
            result = 'n'

        except:
            print("# "+runtext+ " Not Visible")
            result = 'p'

        return result
    
    def xpathWait(xpath,runtext): # 해당 XPATH 값 나타날때까지 대기


        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print("#",runtext)
            n = 0

        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            n = 1
        
        return n
  
    def xpaths(xpath, runtext): # 해당 XPATH 값 유무 확인

        for i in list(range(10)):
            try:
                driver.find_element(By.XPATH,xpath)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()
    
    def xpathClick(xpath, runtext): # 해당 XPATH 클릭
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.XPATH, xpath))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathKey(xpath, key, runtext): # 해당 XPATH 키 입력
        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.ENTER)
                elif key == 'controlA':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.CONTROL,'A')
                elif key == 'backspace':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.BACKSPACE)
                elif key == 'clear':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.CONTROL,'A')
                    time.sleep(1)
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.BACKSPACE)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.XPATH, xpath))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathClear(xpath, runtext): # 해당 XPATH Text 삭제
        for i in list(range(10)):
            try:
                driver.find_element(By.XPATH,xpath).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)

        common.desktopWebError()

    def xpathSelectby(xpath, num, select ,runtext): # 해당 XPATH로 select 제어
        for i in list(range(10)):
            try:
                if num == 0:
                    Select(driver.find_element(By.XPATH, xpath)).select_by_value(select)
                elif num == 1:
                    Select(driver.find_element(By.XPATH, xpath)).select_by_visible_text(select)
                elif num == 2:
                    Select(driver.find_element(By.XPATH, xpath)).select_by_index(select)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathClickSkip(xpath, runtext, runruntext): #해당 XPATH 존재 유무 파악 존재 할 경우 Click

        time.sleep(1)
        try:
            WebDriverWait(driver, 5, poll_frequency=1,
                            ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                EC.presence_of_element_located((By.XPATH, xpath))).click()
            print("# "+runtext+ " Visible")
            print("#",runruntext)
            result = 'p'
        except:
            print("# "+runtext+ " Not Visible")
            result = 'n'
            pass

        return result
        
    def xpathText(xpath, runtext): #해당 XPATH에 있는 TEXT 추출

        try:
            result = driver.find_element(By.XPATH, xpath).text
            print(result)
            print("#",runtext)
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            result = '없음'
            time.sleep(xpathsleep)
        
        return result

    def xpathReturnText(xpath, runtext): #해당 XPATH에 있는 TEXT 추출, 추출한 값 return

        try:
            result = driver.find_element(By.XPATH, xpath).text
            print(result)
            print("#",runtext)

        except Exception as e:
            result = '없음'
            print("Script Execution Error ", "#", runtext)
            print(e)

        return result 

    def xpathDisplayed(xpath,runtext,runruntext): #해당 XPATH가 존재하는지판단 있으면 True 없으면 Fail

        try:
            display = driver.find_element(By.XPATH, xpath).is_displayed()
            print("#",runtext)
            if display == True:
                n = 0
                print(runruntext,' YES')
            else:
                n = 1
                print(runruntext,' NO')
                
            return n
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathSelected(xpath,runtext,runruntext): #해당 XPATH가 선택되어있는지 판단 있으면 True 없으면 Fail
        
        try:
            display = driver.find_element(By.XPATH, xpath).is_selected()
            print("#",runtext)
            if display == True:
                select_YN = 0
                print(runruntext,' YES')
            else:
                select_YN = 1
                print(runruntext,' NO')

            return select_YN
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathReturnAttribute(xpath,value,runtext): #해당 XPATH에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:

            result =driver.find_element(By.XPATH, xpath).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:

            print("Script Execution Error ", "#", runtext)
            print(e)
            result = '없음'
            return result
    
    def xpathclassnameElement(xpath,class_name,runtext): # 해당 XPATH값에 있는 값 확인후 원하는 class 추출

        try:

            a = driver.find_element(By.XPATH,xpath)
            b = a.find_elements(By.CLASS_NAME,class_name)
            c = len(b)
            print('#',runtext)
            return c
        
        except Exception as e:

            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)

    #Css_selector
    def cssSelectorCheck(css_selector, runtext): #해당 Object CSS_SELECTOR의 유무 확인

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorClick(css_selector, runtext): # 해당 CSS_SELECTOR 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorKey(css_selector, key, runtext): # 해당 CSS_SELECTOR 키 입력

        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.CSS_SELECTOR,css_selector).send_keys(Keys.ENTER)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorClear(css_selector, runtext): # 해당 CSS_SELECTOR Text 삭제

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorSelectby(css_selector, visible_text ,runtext): # 해당 CSS_SELECTOR로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.CSS_SELECTOR, css_selector)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorReturnAttribute(css_selector,value,runtext): #해당 XPATH에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:
            result =driver.find_element(By.CSS_SELECTOR, css_selector).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(csssectorsleep)
        common.desktopWebError()

    #Class_Name
    def classNameCheck(class_name, runtext): # 해당 Object CLASS_NAME의 유무 확인
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameClick(class_name, runtext): # 해당 CLASS_NAME 클릭
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameKey(class_name, key, runtext): # 해당 CLASS_NAME 키 입력
        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.CLASS_NAME, class_name).send_keys(Keys.ENTER)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.CLASS_NAME, class_name))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameClear(class_name, runtext): # 해당 CLASS_NAME Text 삭제
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameSelectby(class_name, visible_text ,runtext): # 해당 CLASS_NAME으로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.CLASS_NAME, class_name)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()
    
    def classNameReturnAttribute(class_name,value,runtext): #해당 CLASS_NAME에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:
            result =driver.find_element(By.CLASS_NAME, class_name).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(classname)
        common.desktopWebError()

    #ID
    def idCheck(id, runtext): # 해당 Object ID의 유무 확인
        try:
            driver.find_element(By.ID,id)
            print("# "+runtext+ " Visible")
            result = 'n'

        except:
            print("# "+runtext+ " Not Visible")
            result = 'p'

        return result

    def idClick(id, runtext): # 해당 ID 클릭
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.ID, id))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()

    def idKey(id, key, runtext): # 해당 ID 키 입력
        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.ID,id).send_keys(Keys.ENTER)
                elif key == 'controlA':
                    driver.find_element(By.ID,id).send_keys(Keys.CONTROL,'A')
                elif key == 'backspace':
                    driver.find_element(By.ID,id).send_keys(Keys.BACKSPACE)
                elif key == 'tab':
                    driver.find_element(By.ID,id).send_keys(Keys.TAB)
                elif key == 'clear':
                    driver.find_element(By.ID,id).send_keys(Keys.CONTROL,'A')
                    time.sleep(1)
                    driver.find_element(By.ID,id).send_keys(Keys.BACKSPACE)
                
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.ID, id))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()

    def idClear(id, runtext): # 해당 ID Text 삭제
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.ID, id))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()

    def idSelectby(id, num, select ,runtext): # 해당 ID로 select 제어 num = 0 이면 visible_text 1이면 valus 2이면 index값(num은 int형)
        for i in list(range(10)):
            try:
                if num == 0:
                    Select(driver.find_element(By.ID, id)).select_by_value(select)
                elif num == 1:
                    Select(driver.find_element(By.ID, id)).select_by_visible_text(select)
                elif num == 2:
                    Select(driver.find_element(By.ID, id)).select_by_index(select)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()
    
    def idKeySkip(id, key, runtext, runruntext): #해당 ID 존재 유무 파악 존재 할 경우 Click

        time.sleep(1)
        try:
            WebDriverWait(driver, 5, poll_frequency=1,
                            ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                EC.presence_of_element_located((By.ID, id))).send_keys(key)
            print("# "+runtext+ " Visible")
            print("#",runruntext)
            result = 'p'
        except:
            print("# "+runtext+ " Not Visible")
            result = 'n'
            pass

        return result

    def idReturnText(id, runtext):

        try:
            result = driver.find_element(By.ID, id).text
            print(result)
            print("#",runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()
    
    def idReturnAttribute(id,value,runtext): #해당 ID에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:
            result =driver.find_element(By.ID, id).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()

    def idDisplayed(id,runtext,runruntext):

        try:
            display = driver.find_element(By.ID, id).is_displayed()
            print("#",runtext)
            if display == True:
                n = 0
                print(runruntext,' YES')
            else:
                n = 1
                print(runruntext,' NO')

            return n
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()
    
    def idSelected(id,runtext,runruntext):
        
        try:
            display = driver.find_element(By.ID, id).is_selected()
            print("#",runtext)
            if display == True:
                select_YN = 0
                print(runruntext,' YES')
            else:
                select_YN = 1
                print(runruntext,' NO')

            return select_YN
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()

    def idMoveto(id,runtext): # 해당 ID값에 있는 값 확인 후 좌표 이동
        action = ActionChains(driver)

        for i in list(range(10)):
            try:
                a = driver.find_element(By.ID,id)
                action.move_to_element(a).perform()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()
    
    def idclassnameElement(id,class_name,runtext): # 해당 ID값에 있는 값 확인후 원하는 class 추출

        try:

            a = driver.find_element(By.ID,id)
            b = a.find_elements(By.CLASS_NAME,class_name)
            c = len(b)
            print('#',runtext)
            return c
        
        except Exception as e:

            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)

    #Link_Text
    def linkTextCheck(link_text, runtext): # 해당 Object LINK_TEXT의 유무 확인

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextClick(link_text, runtext): # 해당 LINK_TEXT 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextKey(link_text, key, runtext): # 해당 LINK_TEXT 키 입력

        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.LINK_TEXT,link_text).send_keys(Keys.ENTER)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.LINK_TEXT, link_text))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextClear(link_text, runtext): # 해당 LINK_TEXT Text 삭제

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextSelectby(link_text, visible_text ,runtext): # 해당 LINK_TEXT로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.LINK_TEXT, link_text)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    #Tag_Name
    def tagNameCheck(tag_name, runtext): # 해당 Object TAG_NAME의 유무 확인

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.TAG_NAME, tag_name)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNames(tag_name, runtext): # 해당 TAG_NAME의 값 유무 확인

        try:
            list_value = driver.find_elements(By.TAG_NAME,tag_name)
            print("#",runtext)

        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)
        
        return list_value

    def tagNameClick(tag_name, runtext): # 해당 TAG_NAME 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.TAG_NAME, tag_name))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNameKey(tag_name, key, runtext): # 해당 TAG_NAME 키 입력

        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.TAG_NAME,tag_name).send_keys(Keys.ENTER)
                else:

                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.TAG_NAME, tag_name))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNameClear(tag_name, runtext): # 해당 TAG_NAME 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.TAG_NAME, tag_name))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNameSelectby(tag_name, visible_text ,runtext): # 해당 TAG_NAME로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.TAG_NAME, tag_name)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    # javascriot
    def jsClick(xpath,runtext):

            try:
                
                element = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].click();", element)
                print("#",runtext)

            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)

    def jsScrollo(num,runtext):

        for i in list(range(10)):
            try:

                driver.execute_script("window.scrollTo(0,"+num+")") 
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)

    def jsScrollo_dwon(runtext):

        for i in list(range(10)):
            try:

                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)

    def frameSwitch(runtext): # 프레임 전환(페이지내에 프레임를 검색해서 프레임이 있으면 프레임 전환)

        time.sleep(3)
        try:
            iframes = driver.find_elements(By.CSS_SELECTOR, 'iframe')
            for iframe in iframes:
                frame =iframe.get_attribute('name')
            driver.switch_to.frame(frame)
            print("#",runtext)
            return  frame
        except Exception:
            print("Script Execution Error ", "#", runtext)
            time.sleep(webcommonsleep)
    
    def frameSwitchOrginal(runtext): #원래 프레임으로 전환

        for i in list(range(10)):
            try:
                driver.switch_to.default_content()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()

    def frame(frame,runtext): #프레임 전환(수동)
        
        driver.switch_to.frame(frame)
        print("#",runtext)

    def popupClose(runtext): # 모든 팝업창 닫기(팝업창이 하나 이상일 경우 숫자를 파악해서 모두 닫기)

        for i in list(range(10)):
            try:
                tabs = driver.window_handles
                driver_count = len(driver.window_handles)
                if driver_count != 1:
                    while driver_count >= 2:
                        driver_count = driver_count - 1
                        driver.switch_to.window(driver.window_handles[driver_count]) 
                        driver.close()
                else:
                    pass
                driver.switch_to.window(tabs[0])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()
    
    def popupControl(popup_number,runtext): # 팝업창 제어/popup_number는 팝업창의 갯수 ex)팝업창이 하나 popup_number = 1 팝업창이 둘 popup_number = 2 int형

        for i in list(range(10)):
            try:
                tabs = driver.window_handles
                driver.switch_to.window(tabs[popup_number])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()

    def popupOrginal(runtext): #원래 창으로 전환
        
        for i in list(range(10)):
            try:
                tabs = driver.window_handles
                driver.switch_to.window(tabs[0])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()

    def popupCheck(runtext):

        try:
            tabs = driver.window_handles
            tabs_number = str(len(tabs))
            print('# 현재 팝업창 수: '+tabs_number)
            
            return tabs_number
        except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)

    def alerClose(runtext): # 경고 메세지 닫기 + 경고 메세지 내용 출력

        time.sleep(2)
        try:
            result = driver.switch_to.alert
            alert_text = result.text
            result.accept()
            time.sleep(1)
            print(alert_text)
            print("#",runtext)
            return alert_text
        except Exception:
            print("# No Alert")

    def imageClick(img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 선택하고자 하는 이미지 이름 입력 width_number,Height_number는 int형

        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99
        for i in list(range(5)):
            try:
                path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
                pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
                img = cv2.imread('../../desktop_screenshot.png')
                hoo = cv2.imread(img_path)
                h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
                # 탬플릿 매칭 해내기 
                res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
                threshold = accuracy #정확도 설정
                loc = numpy.where(res >= threshold)
                loc0=loc[0];loc0=loc0[0]
                loc1=loc[1];loc1=loc1[0]
                coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
                print('화면좌표: ', coordinate, '#', runtext)
                pyautogui.click(coordinate)
                time.sleep(2)
                return True
            except Exception as e:
                print('CvScreen Error ', '#', runtext)
                print(e)

    def imageCoordinate(img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 선택하고자 하는 이미지 이름 입력 width_number,Height_number는 int형

        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99
        try:
            path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
            pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
            img = cv2.imread('../../desktop_screenshot.png')
            hoo = cv2.imread(img_path)
            h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
            # 탬플릿 매칭 해내기 
            res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
            threshold = accuracy #정확도 설정
            loc = numpy.where(res >= threshold)
            loc0=loc[0];loc0=loc0[0]
            loc1=loc[1];loc1=loc1[0]
            coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
            print('화면좌표: ', coordinate, '#', runtext)
            time.sleep(2)
            return coordinate
        except Exception as e:
            print('CvScreen Error ', '#', runtext)
            print(e)

    def randomnumber(num, runtext, x=1, n=100): #랜던값 생성 
        # n = 1 상품가격 n = 2 정액형 나머지는 동일(default값 100) num,x,n은 int형
        # x값은 시작하는 수(default값 1)
        # num값은 끝 수
        # 즉 x 이상 num 이하 값을 동일한 확률로 제어

        price_num = random.randrange(9,99)
        a = []
        b = []
        y = 10

        while x < num + 1 :

            a.append(x)
            x = x + 1
            b.append(y)

        randomnumber = random.choices(a, b)
        randomnumber = str(randomnumber[0])

        if n == 1:
            price_num = str(price_num)
            price = price_num + '000'
            print('#',runtext,'-> ',price)
            return price
        elif n == 2:
            discount = randomnumber + '00'
            print('#',runtext,'->',discount)
            return discount
        else:
            print('#',runtext,'->',randomnumber)
            return randomnumber

    def webPyautogui(content,runtext): #pyautogui제어(선택)

        time.sleep(2)
        pyautogui.press(content)
        print('# ',runtext,content+' 선택')

    def webPyautoguiClick(content,runtext): #pyautogui제어(클릭)

        time.sleep(2)
        pyautogui.click(content)
        print('# ',runtext,str(content)+' 선택')

    def webPyautoguiWrite(content,runtext): #pyautogui제어(write)

        time.sleep(2)
        pyautogui.typewrite(content)
        print('# ',runtext)
    
    def error_screenshot(): #오류 스크린샷
        
        path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
        pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
        print('# 오류 스크린샷')

    def weballScreenshot(position,runtext): #스크린샷

        try:
            path =r"img/" + position + ".png"
            url = driver.current_url
            driver.save_screenshot(path)
            print("#",runtext)
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)

    def webScreenshot(position,xpath,runtext): #스크린샷

        path =r"img/" + position + ".png"
        for i in list(range(10)):
            try:
                driver.find_element(By.XPATH,xpath).screenshot(path)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def optional_type(option_number,runtext): #G마켓 선택형

        try:

            option_number = str(option_number)

            # try:
            #     option = driver.find_element(By.XPATH, '//*[@id="optOrderSel_'+option_number+'"]/button').send_keys(Keys.ENTER)
            #     op = 'optOrderSel_'+option_number
                
            # except:
            #     option = driver.find_element(By.XPATH, '//*[@id="optOrderComb_'+option_number+'"]/button').send_keys(Keys.ENTER)
            #     op = 'optOrderComb_'+option_number
            option = driver.find_element(By.XPATH, '//*[@id="optOrderSel_'+option_number+'"]/button|//*[@id="optOrderComb_'+option_number+'"]/button').send_keys(Keys.ENTER)
            time.sleep(1)

            # select = driver.find_element(By.XPATH, '//*[@id="'+op+'"]/ul')
            select = driver.find_element(By.XPATH, '//*[@id="'+'optOrderSel_'+option_number+'"]/ul|//*[@id="'+'optOrderComb_'+option_number+'"]/ul')
            li  = select.find_elements(By.TAG_NAME, 'li')
            li = len(li)
            li = int(li)
            li = li + 1
            num = randrange(1 , li)
            num = str(num)
            select = driver.find_element(By.XPATH, '//*[@id="'+'optOrderSel_'+option_number+'"]/ul/li['+num+']|//*[@id="'+'optOrderComb_'+option_number+'"]/ul/li['+num+']').click()
            time.sleep(1) 
            print('# ',runtext)
        
        except:

            print("Script Execution Error ", "#", runtext)

    def text_type(runtext): #G마켓 텍스트형

        try:
            writing_box = driver.find_element(By.CSS_SELECTOR, '#coreGoodsOption > div.section_option_area > div > div.item_keyin > ul > li > span').text
            time.sleep(1)
            writing_text = driver.find_element(By.XPATH, '//*[@id="optOrderTxtOptValue_0"]').send_keys(writing_box)
            time.sleep(1)
            sun = driver.find_element(By.ID, 'optOrderTxtBtn').click()
            print('# ',runtext)
        
        except:
            print("Script Execution Error ", "#", runtext)

    def calculation_type(runtext): #G마켓 계산형

        try:
            request = driver.find_element(By.CSS_SELECTOR, '#coreGoodsOption > div.section_option_area > div > div.item_autocalc > ul > li > span').text
            r0 = request.split('_')
            r0 = r0[2]
            r0 = r0.split('(')
            r0 = r0[0].replace(' ','')
            r0 = str(r0)
            print(r0)
            request = driver.find_element(By.CSS_SELECTOR, '#coreGoodsOption > div.section_option_area > div > div.item_autocalc > ul > li > span > span').text
            print(request)
            r = request.split('/')
            r1 = r[0]
            rr = r[1]
            r1 = r1.split(':')
            r1 = r1[1].replace(' ','')
            r1 = r1.split(r0)
            r1 = r1[0] # 단위 숫자 
            r2 = rr.split(',')
            r2 = r2[0]
            r3 = rr.split(',')
            r3 = r3[1]
            r2 = r2.split('=')
            r2 = r2[1].replace(' ','') #가로
            r3 = r3.split('=')
            r3 = r3[1].replace(' ','')
            r3 = r3.split(')')
            r3 = r3[0] #세로
            width = driver.find_element(By.ID, 'optOrderTxtCalcValue1').send_keys(r2)
            vertical = driver.find_element(By.ID, 'optOrderTxtCalcValue2').send_keys(r3)
            sun = driver.find_element(By.ID, 'optOrderTxtCalcBtn').click()
            time.sleep(1)
            print('# ',runtext)
        
        except:
            print("Script Execution Error ", "#", runtext)

    def additional_composition(runtext): #G마켓 추가구성
        
        time.sleep(2)
        try:                                        
            add = driver.find_element(By.XPATH, '//*[@id="coreSelectedLi_0"]/button').send_keys(Keys.ENTER)
            time.sleep(1)
            add_button = driver.find_element(By.XPATH, '//*[@id="layer__add-item"]/div[1]/div/div/div/button').send_keys(Keys.ENTER)
            element = driver.find_element(By.XPATH, '//*[@id="layer__add-item"]/div[1]/div/div/div/ul')
            li = element.find_elements(By.TAG_NAME, 'li')
            li = len(li)
            li = int(li)
            li = li + 1
            num = randrange(1 , li)
            num = str(num)
            element = driver.find_element(By.XPATH, '//*[@id="layer__add-item"]/div[1]/div/div/div/ul/li['+num+']').click()
            time.sleep(1)
            ok = driver.find_element(By.ID, 'plusOptionApplyBtn').click()
            print('# ',runtext)

        except:
            print("Script Execution Error ", "#", runtext)

    def new_imagesmilePay(position,img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 스마일페이 보안 결제 전용 나머지는 쓰지말것 
        # 배율 125 % 해상도 7920 X 1080 기준 !!!
        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99

        try:
            path ="img/" + position + ".png" #화면 전체 스크린샷 저장
            # driver.find_element(By.XPATH,xpath).screenshot(path)
            driver.save_screenshot(path)
            # pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
            img = cv2.imread('img/'+position+".png")
            hoo = cv2.imread(img_path)
            h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
            # 탬플릿 매칭 해내기 
            res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
            threshold = accuracy #정확도 설정
            loc = numpy.where(res >= threshold)
            loc0=loc[0];loc0=loc0[0]
            loc1=loc[1];loc1=loc1[0]
            coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
            print('화면좌표: ', coordinate, '#', runtext)
            x = int(coordinate[0])
            y = int(coordinate[1])
            time.sleep(2)
  
                
        except Exception as e:
            print('CvScreen Error ', '#', runtext)
            print(e)

        z = 695
        w = 128
        if z < x < z + w:
            a = 0
        elif z + w < x < z + 2*w:
            a = 1
        elif z + 2*w < x < z + 3*w:
            a = 2
        elif z + 3*w < x < z + 4*w:
            a = 3

        # r = 671
        r = 571
        q = 90
        if r < y < r + q:
            b = 0
        elif r + q < y < r + 2*q:
            b = 1
        elif r + 2*q < y < r + 3*q:
            b = 2

        if a == 0 and b == 0:
            c = 1
        elif a == 1 and b == 0:
            c = 2
        elif a == 2 and b == 0:
            c = 3
        elif a == 3 and b == 0:
            c = 4

        elif a == 0 and b == 1:
            c = 5
        elif a == 1 and b == 1:
            c = 6
        elif a == 2 and b == 1:
            c = 7
        elif a == 3 and b == 1:
            c = 8

        elif a == 0 and b == 2:
            c = 9
        elif a == 1 and b == 2:
            c = 10
        elif a == 2 and b == 2:
            c = 11
        try:

            driver.find_element(By.XPATH,'//*[@id="securityKey"]/button['+str(c)+']').send_keys(Keys.ENTER)
            print('# 문자 인식 성공')

        except:

            print('# 문자 인식 실패')


###################################################################################
# Description : PC mobile Web Browser 을 자동화하기 위한 Class
###################################################################################

class desktopmweb:

    def browserRun(browserName, phone_model, path, runtext): # Browser 명 / 해당 Browser의 경로 / 동선 구간 명칭 등을 입력
        global driver
        for i in list(range(10)):
            try:
                if browserName == 'Chrome': # Browser명이 Chrome인 경우
                    mobile_emulation = { "deviceName": phone_model }
                    chrome_options = webdriver.ChromeOptions()
                    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
                    driver = webdriver.Chrome(path, options=chrome_options)
                    print("#",browserName,runtext)
                    return driver
                elif browserName == 'IE': # Browser명이 IE인 경우
                    ie_options = webdriver.IeOptions()
                    driver = webdriver.Ie(path, options=ie_options)
                    print("#", browserName, runtext)
                    return driver
                else: # Browser명이 지원하지 않는 브라우저인 경우
                    print("Not Support Browser")
                    exit() 
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                exit()
        
    def webaddressConnect(webAddress, runtext): # 접속할 타겟 URL 입력
        for i in list(range(10)):
            try:
                driver.get(webAddress) # 해당 URL 연결
                driver.maximize_window() # 창 최대화
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                driver.quit()
                exit()
    
    def webaddressadditionalConnect(webAddress, runtext): # 접속할 타겟 URL 입력

        for i in list(range(10)):
            try:
                driver.execute_script("window.open("+webAddress+");")
                tabs = driver.window_handles
                driver.switch_to.window(tabs[1])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                driver.quit()
                exit()
    
    def webrefresh(runtext):

        try:

            driver.refresh()
            print('#',runtext)
        
        except:

            print("Script Execution Error ", "#", runtext)
            exit()

    #Xpath
    def xpathCheck(xpath, runtext): # 해당 XPATH 값 유무 확인

        try:
            driver.find_element(By.XPATH,xpath)
            print("# "+runtext+ " Visible")
            result = 'n'

        except:
            print("# "+runtext+ " Not Visible")
            result = 'p'

        return result
    
    def xpathWait(xpath,runtext): # 해당 XPATH 값 나타날때까지 대기


        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
            print("#",runtext)
            n = 0

        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            n = 1
        
        return n
  
    def xpaths(xpath, runtext): # 해당 XPATH 값 유무 확인

        for i in list(range(10)):
            try:
                driver.find_element(By.XPATH,xpath)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()
    
    def xpathClick(xpath, runtext): # 해당 XPATH 클릭
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.XPATH, xpath))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathKey(xpath, key, runtext): # 해당 XPATH 키 입력
        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.ENTER)
                elif key == 'controlA':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.CONTROL,'A')
                elif key == 'backspace':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.BACKSPACE)
                elif key == 'clear':
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.CONTROL,'A')
                    time.sleep(1)
                    driver.find_element(By.XPATH,xpath).send_keys(Keys.BACKSPACE)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.XPATH, xpath))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathClear(xpath, runtext): # 해당 XPATH Text 삭제
        for i in list(range(10)):
            try:
                driver.find_element(By.XPATH,xpath).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)

        common.desktopWebError()

    def xpathSelectby(xpath, num, select ,runtext): # 해당 XPATH로 select 제어
        for i in list(range(10)):
            try:
                if num == 0:
                    Select(driver.find_element(By.XPATH, xpath)).select_by_value(select)
                elif num == 1:
                    Select(driver.find_element(By.XPATH, xpath)).select_by_visible_text(select)
                elif num == 2:
                    Select(driver.find_element(By.XPATH, xpath)).select_by_index(select)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathClickSkip(xpath, runtext, runruntext): #해당 XPATH 존재 유무 파악 존재 할 경우 Click

        time.sleep(1)
        try:
            WebDriverWait(driver, 5, poll_frequency=1,
                            ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                EC.presence_of_element_located((By.XPATH, xpath))).click()
            print("# "+runtext+ " Visible")
            print("#",runruntext)
            result = 'p'
        except:
            print("# "+runtext+ " Not Visible")
            result = 'n'
            pass

        return result
        
    def xpathText(xpath, runtext): #해당 XPATH에 있는 TEXT 추출

        try:
            result = driver.find_element(By.XPATH, xpath).text
            print(result)
            print("#",runtext)
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            result = '없음'
            time.sleep(xpathsleep)
        
        return result

    def xpathReturnText(xpath, runtext): #해당 XPATH에 있는 TEXT 추출, 추출한 값 return

        try:
            result = driver.find_element(By.XPATH, xpath).text
            print(result)
            print("#",runtext)

        except Exception as e:
            result = '없음'
            print("Script Execution Error ", "#", runtext)
            print(e)

        return result 

    def xpathDisplayed(xpath,runtext,runruntext): #해당 XPATH가 존재하는지판단 있으면 True 없으면 Fail

        try:
            display = driver.find_element(By.XPATH, xpath).is_displayed()
            print("#",runtext)
            if display == True:
                n = 0
                print(runruntext,' YES')
            else:
                n = 1
                print(runruntext,' NO')
                
            return n
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathSelected(xpath,runtext,runruntext): #해당 XPATH가 선택되어있는지 판단 있으면 True 없으면 Fail
        
        try:
            display = driver.find_element(By.XPATH, xpath).is_selected()
            print("#",runtext)
            if display == True:
                select_YN = 0
                print(runruntext,' YES')
            else:
                select_YN = 1
                print(runruntext,' NO')

            return select_YN
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)
        common.desktopWebError()

    def xpathReturnAttribute(xpath,value,runtext): #해당 XPATH에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:

            result =driver.find_element(By.XPATH, xpath).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:

            print("Script Execution Error ", "#", runtext)
            print(e)
            result = '없음'
            return result
    
    def xpathclassnameElement(xpath,class_name,runtext): # 해당 XPATH값에 있는 값 확인후 원하는 class 추출

        try:

            a = driver.find_element(By.XPATH,xpath)
            b = a.find_elements(By.CLASS_NAME,class_name)
            c = len(b)
            print('#',runtext)
            return c
        
        except Exception as e:

            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)

    def xpathtagNames(xpath, tag_name, runtext):

        try:

            a = driver.find_element(By.XPATH,xpath)
            b = a.find_elements(By.TAG_NAME,tag_name)
            print('#',runtext)
            return b
        
        except Exception as e:

            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)

    #Css_selector
    def cssSelectorCheck(css_selector, runtext): #해당 Object CSS_SELECTOR의 유무 확인

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorClick(css_selector, runtext): # 해당 CSS_SELECTOR 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorKey(css_selector, key, runtext): # 해당 CSS_SELECTOR 키 입력

        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.CSS_SELECTOR,css_selector).send_keys(Keys.ENTER)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorClear(css_selector, runtext): # 해당 CSS_SELECTOR Text 삭제

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorSelectby(css_selector, visible_text ,runtext): # 해당 CSS_SELECTOR로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.CSS_SELECTOR, css_selector)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(csssectorsleep)
        common.desktopWebError()

    def cssSelectorReturnAttribute(css_selector,value,runtext): #해당 XPATH에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:
            result =driver.find_element(By.CSS_SELECTOR, css_selector).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(csssectorsleep)
        common.desktopWebError()

    #Class_Name
    def classNameCheck(class_name, runtext): # 해당 Object CLASS_NAME의 유무 확인
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameClick(class_name, runtext): # 해당 CLASS_NAME 클릭
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameKey(class_name, key, runtext): # 해당 CLASS_NAME 키 입력
        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.CLASS_NAME, class_name).send_keys(Keys.ENTER)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.CLASS_NAME, class_name))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameClear(class_name, runtext): # 해당 CLASS_NAME Text 삭제
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.CLASS_NAME, class_name))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()

    def classNameSelectby(class_name, visible_text ,runtext): # 해당 CLASS_NAME으로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.CLASS_NAME, class_name)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(classname)
        common.desktopWebError()
    
    def classNameReturnAttribute(class_name,value,runtext): #해당 CLASS_NAME에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:
            result =driver.find_element(By.CLASS_NAME, class_name).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(classname)
        common.desktopWebError()

    #ID
    def idCheck(id, runtext): # 해당 Object ID의 유무 확인
        try:
            driver.find_element(By.ID,id)
            print("# "+runtext+ " Visible")
            result = 'n'

        except:
            print("# "+runtext+ " Not Visible")
            result = 'p'

        return result

    def idClick(id, runtext): # 해당 ID 클릭
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.ID, id))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()

    def idKey(id, key, runtext): # 해당 ID 키 입력
        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.ID,id).send_keys(Keys.ENTER)
                elif key == 'controlA':
                    driver.find_element(By.ID,id).send_keys(Keys.CONTROL,'A')
                elif key == 'backspace':
                    driver.find_element(By.ID,id).send_keys(Keys.BACKSPACE)
                elif key == 'tab':
                    driver.find_element(By.ID,id).send_keys(Keys.TAB)
                elif key == 'clear':
                    driver.find_element(By.ID,id).send_keys(Keys.CONTROL,'A')
                    time.sleep(1)
                    driver.find_element(By.ID,id).send_keys(Keys.BACKSPACE)
                
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.ID, id))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()

    def idClear(id, runtext): # 해당 ID Text 삭제
        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.ID, id))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()

    def idSelectby(id, num, select ,runtext): # 해당 ID로 select 제어 num = 0 이면 visible_text 1이면 valus 2이면 index값(num은 int형)
        for i in list(range(10)):
            try:
                if num == 0:
                    Select(driver.find_element(By.ID, id)).select_by_value(select)
                elif num == 1:
                    Select(driver.find_element(By.ID, id)).select_by_visible_text(select)
                elif num == 2:
                    Select(driver.find_element(By.ID, id)).select_by_index(select)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()
    
    def idKeySkip(id, key, runtext, runruntext): #해당 ID 존재 유무 파악 존재 할 경우 Click

        time.sleep(1)
        try:
            WebDriverWait(driver, 5, poll_frequency=1,
                            ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                EC.presence_of_element_located((By.ID, id))).send_keys(key)
            print("# "+runtext+ " Visible")
            print("#",runruntext)
            result = 'p'
        except:
            print("# "+runtext+ " Not Visible")
            result = 'n'
            pass

        return result

    def idReturnText(id, runtext):

        try:
            result = driver.find_element(By.ID, id).text
            print(result)
            print("#",runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()
    
    def idReturnAttribute(id,value,runtext): #해당 ID에 있는 원하는 값 추출(=원하는 값 value에 기입), 추출한 값 return
        
        try:
            result =driver.find_element(By.ID, id).get_attribute(value)
            print(result)
            print('#',runtext)
            return result
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()

    def idDisplayed(id,runtext,runruntext):

        try:
            display = driver.find_element(By.ID, id).is_displayed()
            print("#",runtext)
            if display == True:
                n = 0
                print(runruntext,' YES')
            else:
                n = 1
                print(runruntext,' NO')

            return n
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()
    
    def idSelected(id,runtext,runruntext):
        
        try:
            display = driver.find_element(By.ID, id).is_selected()
            print("#",runtext)
            if display == True:
                select_YN = 0
                print(runruntext,' YES')
            else:
                select_YN = 1
                print(runruntext,' NO')

            return select_YN
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(idsleep)
        common.desktopWebError()

    def idMoveto(id,runtext): # 해당 ID값에 있는 값 확인 후 좌표 이동
        action = ActionChains(driver)

        for i in list(range(10)):
            try:
                a = driver.find_element(By.ID,id)
                action.move_to_element(a).perform()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(idsleep)
        common.desktopWebError()
    
    def idclassnameElement(id,class_name,runtext): # 해당 ID값에 있는 값 확인후 원하는 class 추출

        try:

            a = driver.find_element(By.ID,id)
            b = a.find_elements(By.CLASS_NAME,class_name)
            c = len(b)
            print('#',runtext)
            return c
        
        except Exception as e:

            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)

    #Link_Text
    def linkTextCheck(link_text, runtext): # 해당 Object LINK_TEXT의 유무 확인

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextClick(link_text, runtext): # 해당 LINK_TEXT 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextKey(link_text, key, runtext): # 해당 LINK_TEXT 키 입력

        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.LINK_TEXT,link_text).send_keys(Keys.ENTER)
                else:
                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.LINK_TEXT, link_text))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextClear(link_text, runtext): # 해당 LINK_TEXT Text 삭제

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.LINK_TEXT, link_text))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(linktextsleep)
        common.desktopWebError()

    def linkTextSelectby(link_text, visible_text ,runtext): # 해당 LINK_TEXT로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.LINK_TEXT, link_text)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    #Tag_Name
    def tagNameCheck(tag_name, runtext): # 해당 Object TAG_NAME의 유무 확인

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.TAG_NAME, tag_name)))
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNames(tag_name, runtext): # 해당 TAG_NAME의 값 유무 확인

        try:
            list_value = driver.find_elements(By.TAG_NAME,tag_name)
            print("#",runtext)

        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)
        
        return list_value

    def tagNameClick(tag_name, runtext): # 해당 TAG_NAME 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.TAG_NAME, tag_name))).click()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNameKey(tag_name, key, runtext): # 해당 TAG_NAME 키 입력

        for i in list(range(10)):
            try:
                if key == 'enter':
                    driver.find_element(By.TAG_NAME,tag_name).send_keys(Keys.ENTER)
                else:

                    WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                        EC.presence_of_element_located((By.TAG_NAME, tag_name))).send_keys(key)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNameClear(tag_name, runtext): # 해당 TAG_NAME 클릭

        for i in list(range(10)):
            try:
                WebDriverWait(driver, 5, poll_frequency=1,
                              ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException]).until(
                    EC.presence_of_element_located((By.TAG_NAME, tag_name))).clear()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)
        common.desktopWebError()

    def tagNameSelectby(tag_name, visible_text ,runtext): # 해당 TAG_NAME로 select 제어
        for i in list(range(10)):
            try:
                Select(driver.find_element(By.TAG_NAME, tag_name)).select_by_visible_text(visible_text)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    # javascriot
    def jsClick(xpath,runtext):

            try:
                
                element = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].click();", element)
                print("#",runtext)

            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)

    def jsScrollo(num,runtext):

        for i in list(range(10)):
            try:

                driver.execute_script("window.scrollTo(0,"+num+")") 
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)

    def jsScrollo_dwon(runtext):

        for i in list(range(10)):
            try:

                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)") 
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(tagname)

    def frameSwitch(runtext): # 프레임 전환(페이지내에 프레임를 검색해서 프레임이 있으면 프레임 전환)

        time.sleep(3)
        try:
            iframes = driver.find_elements(By.CSS_SELECTOR, 'iframe')
            for iframe in iframes:
                frame =iframe.get_attribute('name')
            driver.switch_to.frame(frame)
            print("#",runtext)
            return  frame
        except Exception:
            print("Script Execution Error ", "#", runtext)
            time.sleep(webcommonsleep)
    
    def frameSwitchOrginal(runtext): #원래 프레임으로 전환

        for i in list(range(10)):
            try:
                driver.switch_to.default_content()
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()

    def frame(frame,runtext): #프레임 전환(수동)
        
        driver.switch_to.frame(frame)
        print("#",runtext)

    def popupClose(runtext): # 모든 팝업창 닫기(팝업창이 하나 이상일 경우 숫자를 파악해서 모두 닫기)

        for i in list(range(10)):
            try:
                tabs = driver.window_handles
                driver_count = len(driver.window_handles)
                if driver_count != 1:
                    while driver_count >= 2:
                        driver_count = driver_count - 1
                        driver.switch_to.window(driver.window_handles[driver_count]) 
                        driver.close()
                else:
                    pass
                driver.switch_to.window(tabs[0])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()
    
    def popupControl(popup_number,runtext): # 팝업창 제어/popup_number는 팝업창의 갯수 ex)팝업창이 하나 popup_number = 1 팝업창이 둘 popup_number = 2 int형

        for i in list(range(10)):
            try:
                tabs = driver.window_handles
                driver.switch_to.window(tabs[popup_number])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()

    def popupOrginal(runtext): #원래 창으로 전환
        
        for i in list(range(10)):
            try:
                tabs = driver.window_handles
                driver.switch_to.window(tabs[0])
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)
        common.desktopWebError()

    def popupCheck(runtext):

        try:
            tabs = driver.window_handles
            tabs_number = str(len(tabs))
            print('# 현재 팝업창 수: '+tabs_number)
            
            return tabs_number
        except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(webcommonsleep)

    def alerClose(runtext): # 경고 메세지 닫기 + 경고 메세지 내용 출력

        time.sleep(2)
        try:
            result = driver.switch_to.alert
            alert_text = result.text
            result.accept()
            time.sleep(1)
            print(alert_text)
            print("#",runtext)
            return alert_text
        except Exception:
            print("# No Alert")

    def imageClick(img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 선택하고자 하는 이미지 이름 입력 width_number,Height_number는 int형

        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99
        for i in list(range(5)):
            try:
                path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
                pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
                img = cv2.imread('../../desktop_screenshot.png')
                hoo = cv2.imread(img_path)
                h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
                # 탬플릿 매칭 해내기 
                res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
                threshold = accuracy #정확도 설정
                loc = numpy.where(res >= threshold)
                loc0=loc[0];loc0=loc0[0]
                loc1=loc[1];loc1=loc1[0]
                coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
                print('화면좌표: ', coordinate, '#', runtext)
                pyautogui.click(coordinate)
                time.sleep(2)
                return True
            except Exception as e:
                print('CvScreen Error ', '#', runtext)
                print(e)

    def imageCoordinate(img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 선택하고자 하는 이미지 이름 입력 width_number,Height_number는 int형

        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99
        try:
            path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
            pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
            img = cv2.imread('../../desktop_screenshot.png')
            hoo = cv2.imread(img_path)
            h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
            # 탬플릿 매칭 해내기 
            res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
            threshold = accuracy #정확도 설정
            loc = numpy.where(res >= threshold)
            loc0=loc[0];loc0=loc0[0]
            loc1=loc[1];loc1=loc1[0]
            coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
            print('화면좌표: ', coordinate, '#', runtext)
            time.sleep(2)
            return coordinate
        except Exception as e:
            print('CvScreen Error ', '#', runtext)
            print(e)

    def randomnumber(num, runtext, x=1, n=100): #랜던값 생성 
        # n = 1 상품가격 n = 2 정액형 나머지는 동일(default값 100) num,x,n은 int형
        # x값은 시작하는 수(default값 1)
        # num값은 끝 수
        # 즉 x 이상 num 이하 값을 동일한 확률로 제어

        price_num = random.randrange(9,99)
        a = []
        b = []
        y = 10

        while x < num + 1 :

            a.append(x)
            x = x + 1
            b.append(y)

        randomnumber = random.choices(a, b)
        randomnumber = str(randomnumber[0])

        if n == 1:
            price_num = str(price_num)
            price = price_num + '000'
            print('#',runtext,'-> ',price)
            return price
        elif n == 2:
            discount = randomnumber + '00'
            print('#',runtext,'->',discount)
            return discount
        else:
            print('#',runtext,'->',randomnumber)
            return randomnumber

    def webPyautogui(content,runtext): #pyautogui제어(선택)

        time.sleep(2)
        pyautogui.press(content)
        print('# ',runtext,content+' 선택')

    def webPyautoguiClick(content,runtext): #pyautogui제어(클릭)

        time.sleep(2)
        pyautogui.click(content)
        print('# ',runtext,str(content)+' 선택')

    def webPyautoguiWrite(content,runtext): #pyautogui제어(write)

        time.sleep(2)
        pyautogui.typewrite(content)
        print('# ',runtext)
    
    def error_screenshot(): #오류 스크린샷
        
        path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
        pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
        print('# 오류 스크린샷')

    def weballScreenshot(position,runtext): #스크린샷

        try:
            path =r"img/" + position + ".png"
            url = driver.current_url
            driver.save_screenshot(path)
            print("#",runtext)
        except Exception as e:
            print("Script Execution Error ", "#", runtext)
            print(e)
            time.sleep(xpathsleep)

    def webScreenshot(position,xpath,runtext): #스크린샷

        path =r"img/" + position + ".png"
        for i in list(range(10)):
            try:
                driver.find_element(By.XPATH,xpath).screenshot(path)
                print("#",runtext)
                return True
            except Exception as e:
                print("Script Execution Error ", "#", runtext)
                print(e)
                time.sleep(xpathsleep)
        common.desktopWebError()

    def optional_type(option_number,runtext): #G마켓 선택형

        try:

            option_number = option_number + 1
            driver.find_element(By.XPATH, '//*[@id="scroll_cont_wrap"]/div/div/div['+str(option_number)+']/div/button|//*[@id="scroll_cont_wrap"]/div/div/div['+str(option_number)+']/button').send_keys(Keys.ENTER)
            time.sleep(1)
            option_number = option_number - 1

            # select = driver.find_element(By.XPATH, '//*[@id="'+op+'"]/ul')
            select = driver.find_element(By.XPATH, '//*[@id="'+'selOptionList_'+str(option_number)+'"]/ul|//*[@id="'+'combOptionList_'+str(option_number)+'"]/ul')
            li  = select.find_elements(By.TAG_NAME, 'li')
            li = len(li)
            li = int(li)
            li = li + 1
            num = randrange(1 , li)
            num = str(num)
            select = driver.find_element(By.XPATH, '//*[@id="'+'selOptionList_'+option_number+'"]/ul/li['+num+']|//*[@id="'+'combOptionList_'+option_number+'"]/ul/li['+num+']').click()
            time.sleep(1) 
            print('# ',runtext)
        
        except:

            print("Script Execution Error ", "#", runtext)

    def text_type(runtext): #G마켓 텍스트형

        try:
            writing_box = driver.find_element(By.XPATH, "//label[@for='input_extra_0']").text
            time.sleep(1)
            writing_text = driver.find_element(By.XPATH, "//label[@for='input_extra_0']").send_keys(writing_box)
            time.sleep(1)
            sun = driver.find_element(By.XPATH, '//*[@id="scroll_cont_wrap"]/div/div/div[2]/a').send_keys(Keys.ENTER)
            print('# ',runtext)
        
        except:
            print("Script Execution Error ", "#", runtext)

    def calculation_type(runtext): #G마켓 계산형

        try:
            request = driver.find_element(By.XPATH, '//*[@class="option-item-calculation"]div/span[1]').text
            request = request.replace('\n','')
            r0 = request.split('_')
            r0 = r0[2]
            r0 = r0.split('(')
            r0 = r0[0].replace(' ','')
            r0 = str(r0)
            print(r0)
            request = driver.find_element(By.XPATH, '//*[@class="option-item-calculation"]div/span[1]').text
            print(request)
            r = request.split('/')
            r1 = r[0]
            rr = r[1]
            r1 = r1.split(':')
            r1 = r1[1].replace(' ','')
            r1 = r1.split(r0)
            r1 = r1[0] # 단위 숫자 
            r2 = rr.split(',')
            r2 = r2[0]
            r3 = rr.split(',')
            r3 = r3[1]
            r2 = r2.split('=')
            r2 = r2[1].replace(' ','') #가로
            r3 = r3.split('=')
            r3 = r3[1].replace(' ','')
            r3 = r3.split(')')
            r3 = r3[0] #세로
            width = driver.find_element(By.XPATH, '//*[@class="calculation_box"]/span/input').send_keys(r2)
            vertical = driver.find_element(By.XPATH, '//*[@class="calculation_box"]/div[1]/input').send_keys(r3)
            sun = driver.find_element(By.XPATH, '//*[@id="scroll_cont_wrap"]/div/div/div[4]/a').click()
            time.sleep(1)
            print('# ',runtext)
        
        except:
            print("Script Execution Error ", "#", runtext)

    def additional_composition(runtext): #G마켓 추가구성
        
        time.sleep(2)
        try:                                        
            add = driver.find_element(By.XPATH, '//*[@class="button__add-item sp_vip"]').send_keys(Keys.ENTER)
            time.sleep(1)
            add_button = driver.find_element(By.XPATH, '//*[@id="addOptionContainer"]/div[1]/div/div[1]/button').send_keys(Keys.ENTER)
            element = driver.find_element(By.ID, 'option-add_item_list_0')
            li = element.find_elements(By.TAG_NAME, 'li')
            li = len(li)
            li = int(li)
            li = li + 1
            num = randrange(1 , li)
            num = str(num)
            element = driver.find_element(By.XPATH, '//*[@id="option-add_item_list_0"]/ul/li['+num+']').click()
            time.sleep(1)
            ok = driver.find_element(By.XPATH, '//*[@id="addOptionContainer"]/div[1]/div/div[2]/button').click()
            print('# ',runtext)

        except:
            print("Script Execution Error ", "#", runtext)

    def new_imagesmilePay(position,img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 스마일페이 보안 결제 전용 나머지는 쓰지말것 
        # 배율 125 % 해상도 7920 X 1080 기준 !!!
        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99

        try:
            path ="img/" + position + ".png" #화면 전체 스크린샷 저장
            # driver.find_element(By.XPATH,xpath).screenshot(path)
            driver.save_screenshot(path)
            # pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
            img = cv2.imread('img/'+position+".png")
            hoo = cv2.imread(img_path)
            h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
            # 탬플릿 매칭 해내기 
            res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
            threshold = accuracy #정확도 설정
            loc = numpy.where(res >= threshold)
            loc0=loc[0];loc0=loc0[0]
            loc1=loc[1];loc1=loc1[0]
            coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
            print('화면좌표: ', coordinate, '#', runtext)
            x = int(coordinate[0])
            y = int(coordinate[1])
            time.sleep(2)
  
                
        except Exception as e:
            print('CvScreen Error ', '#', runtext)
            print(e)

        z = 695
        w = 128
        if z < x < z + w:
            a = 0
        elif z + w < x < z + 2*w:
            a = 1
        elif z + 2*w < x < z + 3*w:
            a = 2
        elif z + 3*w < x < z + 4*w:
            a = 3

        # r = 671
        r = 571
        q = 90
        if r < y < r + q:
            b = 0
        elif r + q < y < r + 2*q:
            b = 1
        elif r + 2*q < y < r + 3*q:
            b = 2

        if a == 0 and b == 0:
            c = 1
        elif a == 1 and b == 0:
            c = 2
        elif a == 2 and b == 0:
            c = 3
        elif a == 3 and b == 0:
            c = 4

        elif a == 0 and b == 1:
            c = 5
        elif a == 1 and b == 1:
            c = 6
        elif a == 2 and b == 1:
            c = 7
        elif a == 3 and b == 1:
            c = 8

        elif a == 0 and b == 2:
            c = 9
        elif a == 1 and b == 2:
            c = 10
        elif a == 2 and b == 2:
            c = 11
        try:

            driver.find_element(By.XPATH,'//*[@id="securityKey"]/button['+str(c)+']').send_keys(Keys.ENTER)
            print('# 문자 인식 성공')

        except:

            print('# 문자 인식 실패')


###################################################################################
# Description : PC App 을 자동화하기 위한 Class
###################################################################################


class desktopApp:


    def imageClick(img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 선택하고자 하는 이미지 이름 입력 width_number,Height_number는 int형

        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99
        for i in list(range(10)):
            try:
                path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
                pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
                img = cv2.imread('../../desktop_screenshot.png')
                hoo = cv2.imread(img_path)
                h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
                # 탬플릿 매칭 해내기 
                res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
                threshold = accuracy #정확도 설정
                loc = numpy.where(res >= threshold)
                loc0=loc[0];loc0=loc0[0]
                loc1=loc[1];loc1=loc1[0]
                coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
                print('화면좌표: ', coordinate, '#', runtext)
                pyautogui.click(coordinate)
                time.sleep(2)
                return True
            except Exception as e:
                print('CvScreen Error ', '#', runtext)
                print(e)

        common.desktopAppError()

    def imagedoubleClick(img_path, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 두번 선택하고자 하는 이미지 이름 입력 width_number,Height_number는 int형
        
        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99
        for i in list(range(10)):
            try:
                path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
                pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
                img = cv2.imread('../../desktop_screenshot.png')
                hoo = cv2.imread(img_path)
                h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
                # 탬플릿 매칭 해내기 
                res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
                threshold = accuracy #정확도 설정 
                loc = numpy.where(res >= threshold)
                loc0=loc[0];loc0=loc0[0]
                loc1=loc[1];loc1=loc1[0]
                coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
                print('화면좌표: ', coordinate, '#', runtext)
                pyautogui.doubleClick(coordinate)
                time.sleep(2)
                return True
            except Exception as e:
                print('CvScreen Error ', '#', runtext)
                print(e)

        common.desktopAppError()

    def imageKey(img_path, key, runtext, width_number=1/2,Height_number=1/2, accuracy=0.99): # 선택하고자 하는 이미지 이름 입력 width_number,Height_number는 int형, key값은 타이핑하고자 하는 값(str형)
        
        # width_number, Height_number 는 내가 선택하고자 하는 좌표의 위치값
        # width_number는 x좌표 Height_number는 y좌표를 의미
        # 선택하고자 하는 위치를 분수 형태 0 < width_number,Height_number < 1 로 기입
        # ex) width_number = 1/2 인식한 이미지 x좌표의 1/2지점을 선택
        # Default 값은 1/2,1/2(x좌표의 1/2 , y좌표의 1/2 => 이미지 중앙값)
        # accuracy는 정확도 값 상황에 따라 조절 Default 값은 0.99
        for i in list(range(10)):

            try:
                path =r"..\..\desktop_screenshot.png" #바탕화면에 화면 전체 스크린샷 저장
                pyautogui.screenshot(path, region=(0, 0, 1920, 1080)) #바탕화면 해상도
                img = cv2.imread('../../desktop_screenshot.png')
                hoo = cv2.imread(img_path)
                h,w = hoo.shape[:2] #저장된 사진의 높이 ,넓이 값
                # 탬플릿 매칭 해내기 
                res = cv2.matchTemplate(img, hoo, cv2.TM_CCOEFF_NORMED)
                threshold = accuracy #정확도 설정 
                loc = numpy.where(res >= threshold)
                loc0=loc[0];loc0=loc0[0]
                loc1=loc[1];loc1=loc1[0]
                coordinate = (loc1 + (w * width_number), loc0 + (h * Height_number)) #저장된 사진의 높이 ,넓이 값을 원하는 위치값에 더해서 지정된 사진의 클릭값 도출, 넓이와 높이는 width_number,Height_number 값으로 통제
                pyautogui.click(coordinate)
                print('화면좌표: ', coordinate)
                time.sleep(2)
                pyautogui.typewrite(key)
                time.sleep(2)
                print('#', runtext)
                return True
            except Exception as e:
                print('CvScreen Error ', '#', runtext)
                print(e)
        
        common.desktopAppError()
