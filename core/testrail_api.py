"""TestRail API binding for Python 3.x.

(API v2, available since TestRail 3.0)

Compatible with TestRail 3.0 and later.

Learn more:

http://docs.gurock.com/testrail-api2/start
http://docs.gurock.com/testrail-api2/accessing

Copyright Gurock Software GmbH. See license.md for details.
"""

import base64
import json
import re
import requests

class APIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'


    def send_get(self, uri, filepath=None):
        """Issue a GET request (read) against the API.

        Args:
            uri: The API method to call including parameters, e.g. get_case/1.
            filepath: The path and file name for attachment download; used only
                for 'get_attachment/:attachment_id'.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('GET', uri, filepath)

    def send_post(self, uri, data):
        """Issue a POST request (write) against the API.

        Args:
            uri: The API method to call, including parameters, e.g. add_case/1.
            data: The data to submit as part of the request as a dict; strings
                must be UTF-8 encoded. If adding an attachment, must be the
                path to the file.

        Returns:
            A dict containing the result of the request.
        """
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri

        auth = str(
            base64.b64encode(
                bytes('%s:%s' % (self.user, self.password), 'utf-8')
            ),
            'ascii'
        ).strip()
        headers = {'Authorization': 'Basic ' + auth}

        if method == 'POST':
            if uri[:14] == 'add_attachment':    # add_attachment API method
                files = {'attachment': (open(data, 'rb'))}
                response = requests.post(url, headers=headers, files=files)
                files['attachment'].close()
            else:
                headers['Content-Type'] = 'application/json'
                payload = bytes(json.dumps(data), 'utf-8')
                response = requests.post(url, headers=headers, data=payload)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.get(url, headers=headers)

        if response.status_code > 201:
            try:
                error = response.json()
            except:     # response.content not formatted as JSON
                error = str(response.content)
            raise APIError('TestRail API returned HTTP %s (%s)' % (response.status_code, error))
        else:
            if uri[:15] == 'get_attachment/':   # Expecting file, not JSON
                try:
                    open(data, 'wb').write(response.content)
                    return (data)
                except:
                    return ("Error saving attachment.")
            else:
                try:
                    return response.json()
                except: # Nothing to return
                    return {}



class APIError(Exception):
    pass


class testrailControl:

    def __init__(self,url,id,pw):
        
        self.url = url
        self.id = id
        self.pw = pw

    def get_Case(url,id,pw,number): # 해당 TC Json 파일 불러오기

        client = APIClient(url)
        client.user = id
        client.password = pw

        case = client.send_get('get_case/'+number)

        with open('json/Case_information.json', 'w', encoding='UTF-8') as json_data:
                json.dump(case,json_data,indent="\t", ensure_ascii=False)

        with open("json/Case_information.json", "r", encoding="utf8") as f:
                contents = f.read() 
                json_data = json.loads(contents)

    def update_Case(url,id,pw,number,content): # 해당 TC 수정

            client = APIClient(url)
            client.user = id
            client.password = pw

            case = client.send_post('update_case/'+number,content)

    def post(url,id,pw,position,title,ref,estimate,preconditions,n,content1,expected1,content2=None,expected2=None,content3=None,expected3=None): # TC생성
            
            if n == 0:
                    pass
            elif n == 1:
                    cutoms_step = [
                            {
                            "content": content1,
                            "expected": expected1,
                            "additional_info": "",
                            "refs": ""
                            }
                            ]                 
            elif n == 2:
                    cutoms_step = [
                            {
                                    "content": content1,
                                    "expected": expected1,
                                    "additional_info": "",
                                    "refs": ""
                            },
                            {
                                    "content": content2,
                                    "expected": expected2,
                                    "additional_info": "",
                                    "refs": ""
                            }
                            ]
            elif n == 3:
                    cutoms_step = [
                            {       
                                    "content": content1,
                                    "expected": expected1,
                                    "additional_info": "",
                                    "refs": ""
                            },
                            {
                                    "content": content2,
                                    "expected": expected2,
                                    "additional_info": "",
                                    "refs": ""
                            },
                            {
                                    "content": content3,
                                    "expected": expected3,
                                    "additional_info": "",
                                    "refs": ""
                            }
                            ]
            else:
                    pass
        
            client = APIClient(url)
            client.user = id
            client.password = pw
            result = client.send_post(
            'add_case/'+position+'/1',
            {
            "title": title,
            "refs": ref,
            "type_id": 3,
            "custom_automation_type": 0,
            "estimate": estimate,
            "estimate_forecast": estimate,
            "custom_preconds": preconditions,
            "custom_steps_separated": cutoms_step
            }
            )

            with open('json/New_Case.json', 'w', encoding='UTF-8') as json_data:
                    json.dump(result,json_data,indent="\t", ensure_ascii=False)

            with open("json/New_Case.json", "r", encoding="utf8") as f:
                    contents = f.read() 
                    json_data = json.loads(contents)

            id = json_data['id']

            return id

    def post_attachment(url,id,pw,number,img):

            client = APIClient(url)
            client.user = id
            client.password = pw

            case = client.send_post('add_attachment_to_case/'+number,img+'.png')

            with open('json/Attachment.json', 'w', encoding='UTF-8') as json_data:
                    json.dump(case,json_data,indent="\t", ensure_ascii=False)

            with open("json/Attachment.json", "r", encoding="utf8") as f:
                    contents = f.read() 
                    json_data = json.loads(contents)
            img = json_data['attachment_id']
            img = str(img)
            return img
    
    def post_attachment_result(url,id,pw,number,img):

            client = APIClient(url)
            client.user = id
            client.password = pw

            case = client.send_post('add_attachment_to_result/'+number,img+'.png')
    
    def post_Runtemplate(url,id,pw,position,run_name,number=None,assign=None): #assign는 int

        client = APIClient(url)
        client.user = id
        client.password = pw

        result = client.send_post(
            'add_run/'+position,
            {
                "name": run_name,
                "assignedto_id": assign,
                "include_all" : False,
                "case_ids": number
            }
            )
        
        with open('json/runTemplate.json', 'w', encoding='UTF-8') as json_data:
                json.dump(result,json_data,indent="\t", ensure_ascii=False)

        with open("json/runTemplate.json", "r", encoding="utf8") as f:
                contents = f.read() 
                json_data = json.loads(contents)
        
        run_id = json_data['id']

        return run_id
    
    def get_runId(url,id,pw,number,n): # test runs 값 기입

        client = APIClient(url)
        client.user = id
        client.password = pw

        case = client.send_get('get_tests/'+number)

        with open('json/Run_information.json', 'w', encoding='UTF-8') as json_data:
            json.dump(case,json_data,indent="\t", ensure_ascii=False)

        with open("json/Run_information.json", "r", encoding="utf8") as f:
            contents = f.read() 
            json_data = json.loads(contents)
        id = json_data[n]['id']

        return id
    
    def modify_run(url,id,pw,position,number):

        client = APIClient(url)
        client.user = id
        client.password = pw
        result = client.send_post('update_run/'+position,{
                                    "include_all": False,
                                    "case_ids": number
                                } )

    def post_runResult(url,id,pw,number,result,comment=None): # result는 int형 1.pass 2.blocked 4.retest 5.failed 6.skippedtest 7.stepwaiting

        client = APIClient(url)
        client.user = id
        client.password = pw

        result = client.send_post(
            'add_result/'+number,
            {
            "status_id": result,
            "comment": comment
            }
            )
        
        with open('json/run_result.json', 'w', encoding='UTF-8') as json_data:
                json.dump(result,json_data,indent="\t", ensure_ascii=False)

        with open("json/run_result.json", "r", encoding="utf8") as f:
                contents = f.read() 
                json_data = json.loads(contents)
        
        id = json_data['id']
        id = str(id)

        return id

    def get_Title(url,id,pw,number):

        client = APIClient(url)
        client.user = id
        client.password = pw

        case = client.send_get('get_case/'+number)

        with open('json/Case_information.json', 'w', encoding='UTF-8') as json_data:
                json.dump(case,json_data,indent="\t", ensure_ascii=False)

        with open("json/Case_information.json", "r", encoding="utf8") as f:
                contents = f.read() 
                json_data = json.loads(contents)

        title = json_data['title']
        print(title)

        #회원구분
        if '일반회원' in title:
            Member = 0
        elif '클럽회원' in title:
            Member = 1
        elif '비회원' in title:
            Member = 2
        elif '간편회원' in title:
            Member = 3
        elif 'SFC회원' in title:
            Member = 4
        elif '사업자회원' in title:
            Member = 5
        elif '판매자예치금' in title:
            Member = 6
        elif '일반/클럽' in title:
            Member = 1
        
        if Member == 6:
            goods_Name = 0
            smileCash = 0
            goods_smileCash = 0
            goods_discount = 0
            discount = 0
            coupon = 0 
            double_discount = 0
            goods_buyMethod
            if '신용/체크카드' in title:
                if '현대' in title:
                    goods_buyMethod = 13
                elif '국민' in title:
                    goods_buyMethod = 14
                elif '삼성' in title:
                    goods_buyMethod = 15
                elif '신한' in title:
                    goods_buyMethod = 16
            elif '무통장' in title:
                goods_buyMethod = 17
            elif '판매자 직접 결제' in title or '판매자직접결제' in title or '판매자 직접결제' in title or '판매자직접 결제' in title:
                goods_buyMethod = 18

        else:
            option = 0
            text = 0
            calculation = 0
            addtion = 0
            #상품구분(판매자예치금 상품 제외)
            if '일반상품' in title or '일반배송' in title:
                goods_Name = 1
            elif '도서상품' in title:
                goods_Name = 2
            elif '통관상품' in title:
                goods_Name = 3
            elif '스마일배송' in title:
                goods_Name = 4
            elif '부가세' in title:
                goods_Name = 5
            elif '타이어' in title:
                goods_Name = 6
            elif '100원 상품' in title or '100원상품' in title:
                goods_Name = 7
            elif '방문수령' in title:
                goods_Name = 8
            elif '바우처결제' in title:
                goods_Name = 9
            elif '스마일페이' in title:
                goods_Name = 10
            elif '사은품/덤' in title:
                goods_Name = 11
            elif '성인용품' in title:
                goods_Name = 12
            elif '최대구매제한' in title:
                if '일당' in title:
                    goods_Name = 13
                elif '구매자' in title:
                    goods_Name = 14
            elif 'E쿠폰' in title:
                if '선물하기' in title:
                    goods_Name = 15
                elif '본인인증' in title:
                    goods_Name = 16
            elif '0원상품' in title or '0원 상품' in title or '렌탈' in title:
                    goods_Name = 17
            elif '당일배송' in title:
                goods_Name = 18
            elif '환긍성' in title:
                goods_Name = 19
            elif 'SFC몰' in title:
                goods_Name = 20
            elif 'Biz-on' in title or 'Biz on' in title or 'Biz -on' in title or 'Biz- on' in title or 'Biz - on' in title:
                goods_Name = 21
            elif 'Club biz' in title or 'club biz' in title or 'Club-biz' in title or 'club-biz' in title:
                goods_Name = 22
            elif '더빠른배송' in title or '더빠른 배송' in title:
                if '새벽배송' in title or '새벽' in title:
                    goods_Name = 23
                elif '24시' in title:
                    goods_Name = 24
            elif '환금성' in title:
                goods_Name = 26
            elif '선택형' in title or '2개조합' in title or '3개조합' in title or '2개 조합' in title or '3개 조합' in title:
                goods_Name = 25

                if '선택형' in title:
                    option = 1
                    if '텍스트' in title:
                        text = 2
                    else:
                        text = 1

                    if '계산형' in title:
                        calculation = 2
                    else:
                        calculation = 1
                    
                    if '추가구성' in title:
                        addtion = 2
                    else:
                        addtion = 1
                
                elif '2개조합' in title or '2개 조합' in title:
                    option = 2
                    if '텍스트' in title:
                        text = 2
                    else:
                        text = 1

                    if '계산형' in title:
                        calculation = 2
                    else:
                        calculation = 1
                    
                    if '추가구성' in title:
                        addtion = 2
                    else:
                        addtion = 1
                
                elif '3개조합' in title or '3개 조합' in title:
                    option = 3
                    if '텍스트' in title:
                        text = 2
                    else:
                        text = 1

                    if '계산형' in title:
                        calculation = 2
                    else:
                        calculation = 1
                    
                    if '추가구성' in title:
                        addtion = 2
                    else:
                        addtion = 1
            elif '스마일프레시' in title:
                goods_Name = 27
            else:
                goods_Name = 30

           
            goods_smileCash = 0
            #스마일캐시
            if 'Smile Cash' in title or 'smile cash' in title or 'Smile cash' in title or 'smile Cash' in title:
                smileCash = 1
                a = re.findall(r'\d+',title)
                goods_smileCash = a[-1]
                
            else:
                smileCash = 0

            #할인
            if goods_Name == 16: 
                goods_smileCash = 0
                goods_discount = 0
                discount = 0
                coupon = 0 
                double_discount = 0
            else:
                goods_discount = 0
                discount = 0
                coupon = 0 
                double_discount = 0
            
            if '간편결제' in title:
                sp = 0
            elif '일반결제' in title:
                sp = 1
            else:
                sp = 1
            
            if sp == 0:
                if '캐시충전결제' in title:
                    goods_buyMethod = 6
                elif '신용/체크' in title:
                    if 'T1' in title:
                        goods_buyMethod = 7
                    elif 'T2' in title:
                        goods_buyMethod = 8
                    else:
                        goods_buyMethod = 9
                elif '은행' in title:
                    goods_buyMethod = 10
                elif '휴대폰' in title:
                    goods_buyMethod = 11
                else:
                    goods_buyMethod = 12
            else:
                if '신용/체크카드' in title:
                    goods_buyMethod = 1
                elif '현금결제' in title:
                    goods_buyMethod = 2
                elif '휴대폰' in title:
                    goods_buyMethod = 3
                elif '온누리' in title:
                    goods_buyMethod = 4
                elif 'isp' in title:
                    goods_buyMethod = 5
            
            a = 0
            b = 0
            if '쿠폰' in title:
                if '바이어' in title:
                    a = 1
                elif '마케팅' in title:
                    a = 2
                elif '펀딩' in title:
                    a = 3
            if '판매자할인' in title or '판매자 할인' in title:
                b = 4
            elif '복수구매할인' in title or '복수 구매할인' in title or '복수구매 할인' in title or '복수 구매 할인' in title:
                b = 5
            elif 'Item할인' in title or 'item할인' in title or 'Item 할인' in title or 'item 할인' in title or '아이템 할인' in title or '아이템할인' in title:
                b = 6
            elif '카드사 즉시할인' in title or '카드사즉시할인' in title or '카드사 즉시 할인' in title:
                b = 7
            elif 'PCS' in title:
                b = 8

            if a == 0 and b == 0:
                pass
            elif a != 0 and b != 0:
                double_discount = a
                goods_discount = b

                if b == 8:
                    g = title.split('쿠폰')
                    gg = re.findall(r'\d+',g[1])
                    gg = gg[0]

                    coupon = gg 
                else:
                    x = title.count(',')
                    y = title.count('>')

                    if x > y:
                        z = title.split(',')
                        del z[0], z[0], z[-1]

                    else:
                        z = title.split('>')
                        del z[0], z[0], z[-1]

                    z = z[0].strip()

                    w = re.findall(r'\d+',z)
                    e = w[0]
                    f = w[1]

                    g = z.split('쿠폰')
                    gg = re.findall(r'\d+',g[1])
                    gg = gg[0]

                    if e == f:
                        coupon = e
                        discount = f
                    else:
                        if e == gg:
                            coupon = e
                            discount =f
                        elif f == gg:
                            coupon = f
                            discount = e 

            else:
                if '쿠폰' in title:
                    goods_discount = a
                else:
                    goods_discount = b
                
                if b != 8:
                    x = title.count(',')
                    y = title.count('>')

                    if x > y:
                        z = title.split(',')
                        del z[0], z[0], z[-1]

                    else:
                        z = title.split('>')
                        del z[0], z[0], z[-1]

                    z = z[0].strip()

                    w = re.findall(r'\d+',z)
                    discount = w[0]
                   
        return Member, goods_Name, smileCash, goods_smileCash, goods_discount, discount, coupon, double_discount, goods_buyMethod , option, text, calculation, addtion

    def get_Preconds(url,id,pw,number):

        client = APIClient(url)
        client.user = id
        client.password = pw

        case = client.send_get('get_case/'+number)

        with open('json/Case_information.json', 'w', encoding='UTF-8') as json_data:
                json.dump(case,json_data,indent="\t", ensure_ascii=False)

        with open("json/Case_information.json", "r", encoding="utf8") as f:
                contents = f.read() 
                json_data = json.loads(contents)

        precondition = json_data['custom_preconds']
        print(precondition)

        a = re.findall(r'\d+',precondition)

        goods_buyNumber = a[-1]
        for i in a:

            if int(i) > 1000000000:

                goods_Number = i
            
        b = precondition.split('가격')
        b = b[1]
        b = b.split('원')
        b = b[0]

        if ',' in b:
            b = b.replace(',','')
        c = re.findall(r'\d+',b)
        goods_Price = c[0]

        if '묶음' in precondition:
            deliveryCondition = 1
            if '무료' in precondition:
                goods_deliveryCondition = 1
            elif '유료/선결제' in precondition or '유로/선결제' in precondition:
                goods_deliveryCondition = 2
            elif '유료/착불' in precondition:
                goods_deliveryCondition = 3
            elif '유료/착불&선결제' in precondition:
                goods_deliveryCondition = 4
            elif '조건부/착불&선결제' in precondition:
                goods_deliveryCondition = 5
            elif '조건부/선결제' in precondition:
                goods_deliveryCondition = 6
            elif '조건부/착불' in precondition:
                goods_deliveryCondition = 7
        elif '상품별' in precondition:
            deliveryCondition = 2
            if '무료' in precondition:
                goods_deliveryCondition = 8
            elif '유료/선결제' in precondition:
                goods_deliveryCondition = 9
            elif '조건부/선결제' in precondition:
                goods_deliveryCondition = 10
            elif '수량별차등/구매수량별 반복추가/선결제' in precondition:
                goods_deliveryCondition = 11
            elif '수량별차등/배송비구간직접입력/선결제' in precondition:
                goods_deliveryCondition = 12
        else:
            if '스마일배송' in precondition or '스마일 배송' in precondition:
                deliveryCondition = 3
                if '무료' in precondition:
                    goods_deliveryCondition = 13
                elif '유료' in precondition:
                    goods_deliveryCondition = 14
            elif '방문' in precondition:
                deliveryCondition = 4
                goods_deliveryCondition = 15
            else:
                deliveryCondition = 5
                goods_deliveryCondition = 16

        if '기본' in precondition:
            goods_Delivery = 1
        elif '제주도' in precondition:
            goods_Delivery = 2
        elif '도서' in precondition:
            goods_Delivery = 3

        return goods_Number, goods_Price, goods_buyNumber, goods_deliveryCondition, goods_Delivery, deliveryCondition

    def get_Title_Run(url,id,pw,number):

        client = APIClient(url)
        client.user = id
        client.password = pw

        case = client.send_get('get_test/'+number)

        with open('json/RunCase_information.json', 'w', encoding='UTF-8') as json_data:
                json.dump(case,json_data,indent="\t", ensure_ascii=False)

        with open("json/RunCase_information.json", "r", encoding="utf8") as f:
                contents = f.read() 
                json_data = json.loads(contents)

        title = json_data['title']
        print(title)

        #회원구분
        if '일반회원' in title:
            Member = 0
        elif '클럽회원' in title:
            Member = 1
        elif '비회원' in title:
            Member = 2
        elif '간편회원' in title:
            Member = 3
        elif 'SFC회원' in title:
            Member = 4
        elif '사업자회원' in title:
            Member = 5
        elif '판매자예치금' in title:
            Member = 6
        elif '일반/클럽' in title:
            Member = 1
        
        if Member == 6:
            goods_Name = 0
            smileCash = 0
            goods_smileCash = 0
            goods_discount = 0
            discount = 0
            coupon = 0 
            double_discount = 0
            goods_buyMethod
            if '신용/체크카드' in title:
                if '현대' in title:
                    goods_buyMethod = 13
                elif '국민' in title:
                    goods_buyMethod = 14
                elif '삼성' in title:
                    goods_buyMethod = 15
                elif '신한' in title:
                    goods_buyMethod = 16
            elif '무통장' in title:
                goods_buyMethod = 17
            elif '판매자 직접 결제' in title or '판매자직접결제' in title or '판매자 직접결제' in title or '판매자직접 결제' in title:
                goods_buyMethod = 18

        else:
            option = 0
            text = 0
            calculation = 0
            addtion = 0
            #상품구분(판매자예치금 상품 제외)
            if '일반상품' in title or '일반배송' in title:
                goods_Name = 1
            elif '도서상품' in title:
                goods_Name = 2
            elif '통관상품' in title:
                goods_Name = 3
            elif '스마일배송' in title:
                goods_Name = 4
            elif '부가세' in title:
                goods_Name = 5
            elif '타이어' in title:
                goods_Name = 6
            elif '100원 상품' in title or '100원상품' in title:
                goods_Name = 7
            elif '방문수령' in title:
                goods_Name = 8
            elif '바우처결제' in title:
                goods_Name = 9
            elif '스마일페이' in title:
                goods_Name = 10
            elif '사은품/덤' in title:
                goods_Name = 11
            elif '성인용품' in title:
                goods_Name = 12
            elif '최대구매제한' in title:
                if '일당' in title:
                    goods_Name = 13
                elif '구매자' in title:
                    goods_Name = 14
            elif 'E쿠폰' in title:
                if '선물하기' in title:
                    goods_Name = 15
                elif '본인인증' in title:
                    goods_Name = 16
            elif '0원상품' in title or '0원 상품' in title or '렌탈' in title:
                    goods_Name = 17
            elif '당일배송' in title:
                goods_Name = 18
            elif '환긍성' in title:
                goods_Name = 19
            elif 'SFC몰' in title:
                goods_Name = 20
            elif 'Biz-on' in title or 'Biz on' in title or 'Biz -on' in title or 'Biz- on' in title or 'Biz - on' in title:
                goods_Name = 21
            elif 'Club biz' in title or 'club biz' in title or 'Club-biz' in title or 'club-biz' in title:
                goods_Name = 22
            elif '더빠른배송' in title or '더빠른 배송' in title:
                if '새벽배송' in title or '새벽' in title:
                    goods_Name = 23
                elif '24시' in title:
                    goods_Name = 24
            elif '환금성' in title:
                goods_Name = 26
            elif '선택형' in title or '2개조합' in title or '3개조합' in title or '2개 조합' in title or '3개 조합' in title:
                goods_Name = 25

                if '선택형' in title:
                    option = 1
                    if '텍스트' in title:
                        text = 2
                    else:
                        text = 1

                    if '계산형' in title:
                        calculation = 2
                    else:
                        calculation = 1
                    
                    if '추가구성' in title:
                        addtion = 2
                    else:
                        addtion = 1
                
                elif '2개조합' in title or '2개 조합' in title:
                    option = 2
                    if '텍스트' in title:
                        text = 2
                    else:
                        text = 1

                    if '계산형' in title:
                        calculation = 2
                    else:
                        calculation = 1
                    
                    if '추가구성' in title:
                        addtion = 2
                    else:
                        addtion = 1
                
                elif '3개조합' in title or '3개 조합' in title:
                    option = 3
                    if '텍스트' in title:
                        text = 2
                    else:
                        text = 1

                    if '계산형' in title:
                        calculation = 2
                    else:
                        calculation = 1
                    
                    if '추가구성' in title:
                        addtion = 2
                    else:
                        addtion = 1
            elif '스마일프레시' in title:
                goods_Name = 27
            else:
                goods_Name = 30

           
            goods_smileCash = 0
            #스마일캐시
            if 'Smile Cash' in title or 'smile cash' in title or 'Smile cash' in title or 'smile Cash' in title:
                smileCash = 1
                a = re.findall(r'\d+',title)
                goods_smileCash = a[-1]
                
            else:
                smileCash = 0

            #할인
            if goods_Name == 16: 
                goods_smileCash = 0
                goods_discount = 0
                discount = 0
                coupon = 0 
                double_discount = 0
            else:
                goods_discount = 0
                discount = 0
                coupon = 0 
                double_discount = 0
            
            if '간편결제' in title:
                sp = 0
            elif '일반결제' in title:
                sp = 1
            else:
                sp = 1
            
            if sp == 0:
                if '캐시충전결제' in title:
                    goods_buyMethod = 6
                elif '신용/체크' in title:
                    if 'T1' in title:
                        goods_buyMethod = 7
                    elif 'T2' in title:
                        goods_buyMethod = 8
                    else:
                        goods_buyMethod = 9
                elif '은행' in title:
                    goods_buyMethod = 10
                elif '휴대폰' in title:
                    goods_buyMethod = 11
                else:
                    goods_buyMethod = 12
            else:
                if '신용/체크카드' in title:
                    goods_buyMethod = 1
                elif '현금결제' in title:
                    goods_buyMethod = 2
                elif '휴대폰' in title:
                    goods_buyMethod = 3
                elif '온누리' in title:
                    goods_buyMethod = 4
                elif 'isp' in title:
                    goods_buyMethod = 5
            
            a = 0
            b = 0
            if '쿠폰' in title:
                if '바이어' in title:
                    a = 1
                elif '마케팅' in title:
                    a = 2
                elif '펀딩' in title:
                    a = 3
            if '판매자할인' in title or '판매자 할인' in title:
                b = 4
            elif '복수구매할인' in title or '복수 구매할인' in title or '복수구매 할인' in title or '복수 구매 할인' in title:
                b = 5
            elif 'Item할인' in title or 'item할인' in title or 'Item 할인' in title or 'item 할인' in title or '아이템 할인' in title or '아이템할인' in title:
                b = 6
            elif '카드사 즉시할인' in title or '카드사즉시할인' in title or '카드사 즉시 할인' in title:
                b = 7
            elif 'PCS' in title:
                b = 8

            if a == 0 and b == 0:
                pass
            elif a != 0 and b != 0:
                double_discount = a
                goods_discount = b

                if b == 8:
                    g = title.split('쿠폰')
                    gg = re.findall(r'\d+',g[1])
                    gg = gg[0]

                    coupon = gg 
                else:
                    x = title.count(',')
                    y = title.count('>')

                    if x > y:
                        z = title.split(',')
                        del z[0], z[0], z[-1]

                    else:
                        z = title.split('>')
                        del z[0], z[0], z[-1]

                    z = z[0].strip()

                    w = re.findall(r'\d+',z)
                    e = w[0]
                    f = w[1]

                    g = z.split('쿠폰')
                    gg = re.findall(r'\d+',g[1])
                    gg = gg[0]

                    if e == f:
                        coupon = e
                        discount = f
                    else:
                        if e == gg:
                            coupon = e
                            discount = f
                        elif f == gg:
                            coupon = f
                            discount = e 

            else:
                if '쿠폰' in title:
                    goods_discount = a
                else:
                    goods_discount = b
                
                if b != 8:
                    x = title.count(',')
                    y = title.count('>')

                    if x > y:
                        z = title.split(',')
                        del z[0], z[0], z[-1]

                    else:
                        z = title.split('>')
                        del z[0], z[0], z[-1]

                    z = z[0].strip()

                    w = re.findall(r'\d+',z)
                    discount = w[0]
                   
        return Member, goods_Name, smileCash, goods_smileCash, goods_discount, discount, coupon, double_discount, goods_buyMethod , option, text, calculation, addtion

    def get_Preconds_Run(url,id,pw,number):

        client = APIClient(url)
        client.user = id
        client.password = pw

        case = client.send_get('get_test/'+number)

        with open('json/RunCase_information.json', 'w', encoding='UTF-8') as json_data:
                json.dump(case,json_data,indent="\t", ensure_ascii=False)

        with open("json/RunCase_information.json", "r", encoding="utf8") as f:
                contents = f.read() 
                json_data = json.loads(contents)

        precondition = json_data['custom_preconds']
        print(precondition)

        a = re.findall(r'\d+',precondition)

        goods_buyNumber = a[-1]
        for i in a:

            if int(i) > 1000000000:

                goods_Number = i
            
        b = precondition.split('가격')
        b = b[1]
        b = b.split('원')
        b = b[0]

        if ',' in b:
            b = b.replace(',','')
        c = re.findall(r'\d+',b)
        goods_Price = c[0]

        if '묶음' in precondition:
            deliveryCondition = 1
            if '무료' in precondition:
                goods_deliveryCondition = 1
            elif '유료/선결제' in precondition or '유로/선결제' in precondition:
                goods_deliveryCondition = 2
            elif '유료/착불' in precondition:
                goods_deliveryCondition = 3
            elif '유료/착불&선결제' in precondition:
                goods_deliveryCondition = 4
            elif '조건부/착불&선결제' in precondition:
                goods_deliveryCondition = 5
            elif '조건부/선결제' in precondition:
                goods_deliveryCondition = 6
            elif '조건부/착불' in precondition:
                goods_deliveryCondition = 7
        elif '상품별' in precondition:
            deliveryCondition = 2
            if '무료' in precondition:
                goods_deliveryCondition = 8
            elif '유료/선결제' in precondition:
                goods_deliveryCondition = 9
            elif '조건부/선결제' in precondition:
                goods_deliveryCondition = 10
            elif '수량별차등/구매수량별 반복추가/선결제' in precondition:
                goods_deliveryCondition = 11
            elif '수량별차등/배송비구간직접입력/선결제' in precondition:
                goods_deliveryCondition = 12
        else:
            if '스마일배송' in precondition or '스마일 배송' in precondition:
                deliveryCondition = 3
                if '무료' in precondition:
                    goods_deliveryCondition = 13
                elif '유료' in precondition:
                    goods_deliveryCondition = 14
            elif '방문' in precondition:
                deliveryCondition = 4
                goods_deliveryCondition = 15
            else:
                deliveryCondition = 5
                goods_deliveryCondition = 16

        if '기본' in precondition:
            goods_Delivery = 1
        elif '제주도' in precondition:
            goods_Delivery = 2
        elif '도서' in precondition:
            goods_Delivery = 3

        return goods_Number, goods_Price, goods_buyNumber, goods_deliveryCondition, goods_Delivery, deliveryCondition

