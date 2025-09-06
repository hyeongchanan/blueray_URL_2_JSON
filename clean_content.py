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
#쿠팡
url = 'https://www.yes24.com/product/search?domain=ALL&query=Toy%20Story%20%281995%29'
url1 ="https://www.yes24.com/product/search?domain=ALL&query=Grumpier%20Old%20Men%20%281995%29"
url2 ="https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=DVD&SearchWord=Toy%20Story%20%281995%29"
url3="https://www.dvd.co.kr/shop/shopbrand.html?search=Toy%20Story%20%281995%29"
url4="https://search.kyobobook.co.kr/search?keyword=Toy%20Story%20%281995%29"

cleaned_text = clean_content(url)
text = "안녕하세요! 이것은 파일에 쓰는 예제입니다."

# 'w' 모드는 파일을 새로 쓰거나 기존 내용을 덮어씀
with open("example.txt", "w", encoding="utf-8") as f:
    f.write(cleaned_text)

print("파일에 텍스트가 저장되었습니다.")
