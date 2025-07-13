import requests
from bs4 import BeautifulSoup



#url 입력받아서 상품 정보텍스트를 추출
def clean_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 1. 기본 태그 제거
    base_tags = ['header', 'footer', 'nav', 'aside', 'script', 
                'style', 'noscript','button']
    for tag in base_tags:
        for element in soup.find_all(tag):
            element.decompose()
    
    # 2. 속성 기반 제거 (CSS 선택자 사용)
    attribute_selectors = [
        # yes 24 용 제거 id
        '[id*="trend"]', '[class*="trend"]',
        '[id*="filter"]', '[class*="filter"]',
        '[id*="Filter"]', '[class*="Filter"]',
        '[id*="Header"]', '[class*="Header"]',

        # 알라딘용 제거 id
        '[id*="Search3_Left_Division"]', '[class*="Search3_Left_Division"]',
        '[id*="nav"]', '[class*="nav"]',
        '[id*="evaluate"]', '[class*="evaluate"]',
        
        # 교보문교용 제거 id
        '[id*="faq"]', '[class*="faq"]',


        #11번가용
        '[id*="store_category"]', '[class*="store_category"]',

        '[id*="btn"]', '[class*="btn"]',
        '[id*="button"]', '[class*="button"]',

        '[id*="header"]', '[class*="header"]',    # 헤더 관련
        '[id*="footer"]', '[class*="footer"]',    # 푸터 관련
        '[id*="menu"]', '[class*="menu"]',        # 메뉴
        '[id*="modal"]', '[class*="modal"]',      # 팝업
        #'[id*="banner"]', '[class*="banner"]',    # 배너
        '[role="navigation"]', '[role="banner"]'  # ARIA 역할
    ]
    for selector in attribute_selectors:
        for element in soup.select(selector):
            element.decompose()
    
    # 3. 텍스트 청소 강화
    for element in soup.find_all(string=lambda text: isinstance(text, str)):
        stripped = element.strip()
        if not stripped or stripped in ('\n', '\r', '\t'):
            element.extract()
    
    # 4. 빈 부모 태그 재귀적 제거
    def remove_empty_parents(tag):
        while tag.parent and not tag.parent.text.strip():
            tag = tag.parent
            tag.decompose()
    
    for tag in soup.find_all():
        if not tag.text.strip() and not tag.attrs:
            remove_empty_parents(tag)
    
    return soup.get_text(separator='\n', strip=True)

# 사용 예시
#알라딘
url = 'https://www.yes24.com/product/search?domain=DVD&query=%25EB%25A6%25B4%25EB%25A1%259C%25EC%2599%2580%2520%25EC%258A%25A4%25ED%258B%25B0%25EC%25B9%2598%2520%25EB%25B8%2594%25EB%25A3%25A8%25EB%25A0%2588%25EC%259D%25B4'
#yes24
url2='https://www.yes24.com/product/search?domain=ALL&query=%25EB%25A6%25B4%25EB%25A1%259C%25EC%2599%2580%2520%25EC%258A%25A4%25ED%258B%25B0%25EC%25B9%2598%2520%25EB%25B8%2594%25EB%25A3%25A8%25EB%25A0%2588%25EC%259D%25B4'
#G마켓
url3='https://minishop.gmarket.co.kr/yes24/List?Category=300020728&CategoryType=General&SortType=NewlyListed&DisplayType=SmallImage&Page=0&PageSize=60&IsFreeShipping=False&HasDiscount=False&HasStamp=False&HasMileage=False&IsInternationalShipping=False&MinPrice=200&MaxPrice=14838800'

#페이시아    잘 안됨 상품명이 아랍어? 로 나옴
url4='https://www.peysia.co.kr/shop/shopbrand.html?search=%BA%ED%B7%E7%B7%B9%C0%CC&refer=https:'

#김치 디비디
url5='https://kr.kimchidvd.com:444/kr/goods/search.kimchi?searchWrd=%EB%B8%94%EB%A3%A8%EB%A0%88%EC%9D%B4&media=&searchCnd=kor_title'
#교보문고
url6='https://search.kyobobook.co.kr/search?keyword=%EB%B8%94%EB%A3%A8%EB%A0%88%EC%9D%B4&gbCode=TOT&target=total'

#11번가
url7='https://shop.11st.co.kr/stores/340289/category?isCategory=true&categoryType=DISPLAY&dispCtgrNo=3141&largeCtgrNo=2967&middleCtgrNo=3141&sortCd=N&filter=&pageNo=1'
cleaned_text = clean_content(url)
#print(cleaned_text)