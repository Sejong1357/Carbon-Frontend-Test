
# G마켓
goods_deliveryCondition = 2
goods_Delivery = 1
deliveryCondition = 1
Member = 0
goods_Name = 1
smileCash = 0
goods_smileCash = 0
goods_discount = 5
discount = 2
double_discount = 1
coupon = 100
goods_buyMethod = 6

# 옵션 상품
option = 0
text = 0
calculation = 0
addtion = 0


def members(x):

    if '일반회원' in x:
        Member = 0
        gmarket_id = ['sejong147']
    elif '클럽회원' in x:
        Member = 1
        gmarket_id = ['sejong147']
    elif '비회원' in x:
        Member = 2
        gmarket_id = ['없음']
    elif '간편회원' in x:
        Member = 3
        gmarket_id = ['sejong741']
    elif 'SFC회원' in x:
        Member = 4
        gmarket_id = ['testsfc']
    elif '사업자회원' in x:
        Member = 5
        gmarket_id = ['test4dev']
    elif '판매자예치금' in x:
        Member = 6
        gmarket_id = ['없음']
    elif '일반/클럽' in x:
        Member = 1
        gmarket_id = ['sejong147']
    
    return Member, gmarket_id

def goodsName(x):

    option = 0
    text = 0
    calculation = 0
    addtion = 0
    #상품구분(판매자예치금 상품 제외)
    if '일반상품' in x or '일반배송' in x:
        goods_Name = 1
    elif '도서상품' in x:
        goods_Name = 2
    elif '통관상품' in x:
        goods_Name = 3
    elif '스마일배송' in x:
        goods_Name = 4
    elif '부가세' in x:
        goods_Name = 5
    elif '타이어' in x:
        goods_Name = 6
    elif '100원 상품' in x or '100원상품' in x:
        goods_Name = 7
    elif '방문수령' in x:
        goods_Name = 8
    elif '바우처결제' in x:
        goods_Name = 9
    elif '스마일페이' in x:
        goods_Name = 10
    elif '사은품/덤' in x:
        goods_Name = 11
    elif '성인용품' in x:
        goods_Name = 12
    elif '최대구매제한' in x:
        if '일당' in x:
            goods_Name = 13
        elif '구매자' in x:
            goods_Name = 14
    elif 'E쿠폰' in x:
        if '선물하기' in x:
            goods_Name = 15
        elif '본인인증' in x:
            goods_Name = 16
    elif '0원상품' in x or '0원 상품' in x or '렌탈' in x:
            goods_Name = 17
    elif '당일배송' in x:
        goods_Name = 18
    elif '환긍성' in x:
        goods_Name = 19
    elif 'SFC몰' in x:
        goods_Name = 20
    elif 'Biz-on' in x or 'Biz on' in x or 'Biz -on' in x or 'Biz- on' in x or 'Biz - on' in x:
        goods_Name = 21
    elif 'Club biz' in x or 'club biz' in x or 'Club-biz' in x or 'club-biz' in x:
        goods_Name = 22
    elif '더빠른배송' in x or '더빠른 배송' in x:
        if '새벽배송' in x:
            goods_Name = 23
        elif '24시' in x:
            goods_Name = 24
    elif '선택형' in x or '2개조합' in x or '3개조합' in x or '2개 조합' in x or '3개 조합' in x:
        goods_Name = 25

        if '선택형' in x:
            option = 1
            if '텍스트' in x:
                text = 2
            else:
                text = 1

            if '계산형' in x:
                calculation = 2
            else:
                calculation = 1
            
            if '추가구성' in x:
                addtion = 2
            else:
                addtion = 1
        
        elif '2개조합' in x or '2개 조합' in x:
            option = 2
            if '텍스트' in x:
                text = 2
            else:
                text = 1

            if '계산형' in x:
                calculation = 2
            else:
                calculation = 1
            
            if '추가구성' in x:
                addtion = 2
            else:
                addtion = 1
        
        elif '3개조합' in x or '3개 조합' in x:
            option = 3
            if '텍스트' in x:
                text = 2
            else:
                text = 1

            if '계산형' in x:
                calculation = 2
            else:
                calculation = 1
            
            if '추가구성' in x:
                addtion = 2
            else:
                addtion = 1
    elif '스마일프레시' in x:
            goods_Name = 27
    else:
        goods_Name = 30
    
    return goods_Name, option, text, calculation, addtion

def all_Discount(x,z,y,w):

    
    if '쿠폰' in x:
        if '바이어' in x:
            a = 1
        elif '마케팅' in x:
            a = 2
        elif '펀딩' in x:
            a = 3
    else:
        a = 0
    if '판매자할인' in y or '판매자 할인' in y:
        b = 4
    elif '복수구매할인' in y or '복수 구매할인' in y or '복수구매 할인' in y or '복수 구매 할인' in y:
        b = 5
    elif 'Item할인' in y or 'item할인' in y or 'Item 할인' in y or 'item 할인' in y or '아이템 할인' in y or '아이템할인' in y:
        b = 6
    elif '카드사 즉시할인' in y or '카드사즉시할인' in y or '카드사 즉시 할인' in y:
        b = 7
    elif 'PCS' in y:
        b = 8
    else:
        b = 0
    
    double_discount = a 
    goods_discount= b
    coupon = z
    discount = w

    return double_discount, goods_discount, coupon, discount

def SmileCash(x,y = 0):

    if 'y' in x or 'yes' in x or '있음' in x:
        smileCash = 1
        goods_smileCash = y
    else:
        smileCash = 0
        goods_smileCash = y
    
    return smileCash ,goods_smileCash
    
def buyMethod(x):

    if '간편결제' in x:
        sp = 0
    elif '일반결제' in x:
        sp = 1
    else:
        sp = 1
    
    if sp == 0:
        if '캐시충전결제' in x:
            goods_buyMethod = 6
        elif '신용/체크' in x:
            if 'T1' in x:
                goods_buyMethod = 7
            elif 'T2' in x:
                goods_buyMethod = 8
            else:
                goods_buyMethod = 9
        elif '은행' in x:
            goods_buyMethod = 10
        elif '휴대폰' in x:
            goods_buyMethod = 11
        else:
            goods_buyMethod = 12
    else:
        if '신용/체크카드' in x:
            goods_buyMethod = 1
        elif '현금결제' in x:
            goods_buyMethod = 2
        elif '휴대폰' in x:
            goods_buyMethod = 3
        elif '온누리' in x:
            goods_buyMethod = 4
        elif 'isp' in x:
            goods_buyMethod = 5
    
    return goods_buyMethod

def delivery_Condition(x):

    if '묶음' in x:
        deliveryCondition = 1
        if '무료' in x:
            goods_deliveryCondition = 1
        elif '유료/선결제' in x or '유로/선결제' in x:
            goods_deliveryCondition = 2
        elif '유료/착불' in x:
            goods_deliveryCondition = 3
        elif '유료/착불&선결제' in x:
            goods_deliveryCondition = 4
        elif '조건부/착불&선결제' in x:
            goods_deliveryCondition = 5
        elif '조건부/선결제' in x:
            goods_deliveryCondition = 6
        elif '조건부/착불' in x:
            goods_deliveryCondition = 7
    elif '상품별' in x:
        deliveryCondition = 2
        if '무료' in x:
            goods_deliveryCondition = 8
        elif '유료/선결제' in x:
            goods_deliveryCondition = 9
        elif '조건부/선결제' in x:
            goods_deliveryCondition = 10
        elif '수량별차등/구매수량별 반복추가/선결제' in x:
            goods_deliveryCondition = 11
        elif '수량별차등/배송비구간직접입력/선결제' in x:
            goods_deliveryCondition = 12
    else:
        if '스마일배송' in x or '스마일 배송' in x:
            deliveryCondition = 3
            if '무료' in x:
                goods_deliveryCondition = 13
            elif '유료' in x:
                goods_deliveryCondition = 14
        elif '방문' in x:
            deliveryCondition = 4
            goods_deliveryCondition = 15
        else:
            deliveryCondition = 5
            goods_deliveryCondition = 16
    
    return deliveryCondition, goods_deliveryCondition

def Delivery(x):

    if '기본' in x:
        goods_Delivery = 1
    elif '제주도' in x:
        goods_Delivery = 2
    elif '도서' in x:
        goods_Delivery = 3
    
    return goods_Delivery

# 회원, 상품이름, 할인, 스마일캐쉬, 구매방법, 배송조건, 배송지
def condition(a,b,c,d,e,f,g,h,i,j,k):

    Member, gmarket_id = members(a)

    goods_Name, option, text, calculation, addtion = goodsName(b)

    double_discount, goods_discount, coupon, discount = all_Discount(c,d,e,f)

    smileCash ,goods_smileCash = SmileCash(g,h)

    goods_buyMethod = buyMethod(i)

    deliveryCondition, goods_deliveryCondition = delivery_Condition(j)

    goods_Delivery = Delivery(k)

    return Member, goods_Name, option, text, calculation, addtion, double_discount, goods_discount, coupon, discount, smileCash ,goods_smileCash, goods_buyMethod, deliveryCondition, goods_deliveryCondition, goods_Delivery, gmarket_id





