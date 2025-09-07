import requests
from bs4 import BeautifulSoup



def clean_content_extract(url):
    """
    url: 크롤링할 페이지 URL
    selectors: 추출하고 싶은 태그 CSS 선택자 리스트
    remove_selectors: 선택한 태그 내부에서 제거할 태그 CSS 선택자 리스트
    """
    selectors = [
        # yes24 용
        'div.item_info',
        # 알라딘용
        'div.ss_book_list',
        # 교보문고용
        'ul.prod_list div.horizontal'
    ]

    remove_selectors = [
        # yes24 용
        '*.bgYUI',
        'span.yPoint',
        'span.iconC',
        'em.yes_b',
        'span.authPub',
        #알라딘용
        'span.ss_p',
        #교보
        'div.auto_overflow_footer',
        'span.date',
        'span.price_normal',
        'span.percent',
        'span.point',
        'div.prod_bottom',
        'div.auto_overflow_footer',
        'div.prod_thumb_box',
        'ul.swiper-wrapper'
    ]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    extracted_texts = []

    for selector in selectors:
        for element in soup.select(selector):
            # 내부에서 제거할 태그 처리
            if remove_selectors:
                for remove_selector in remove_selectors:
                    for unwanted in element.select(remove_selector):
                        unwanted.decompose()
            
            # 화면 순서대로 텍스트 추출
            text = element.get_text(separator='\n', strip=True)
            if text:
                extracted_texts.append(text)
    
    return '\n'.join(extracted_texts)
"""

# 사용 예시
url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=DVD&SearchWord=asdfasdf'

# 추출하고 싶은 태그/클래스/ID 지정

extracted_text = clean_context_extract(url)

with open("extracted_example.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("선택한 태그의 텍스트가 파일에 저장되었습니다.")
"""