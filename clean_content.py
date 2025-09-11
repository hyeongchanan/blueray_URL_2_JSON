import requests
from bs4 import BeautifulSoup

yes_selector = 'div.itemUnit'

yes_name = 'a.gd_name'
yes_lnk = 'a.lnk_img'
yes_img = 'img.gImg'
yes_price = 'em.yes_b'

ala_selector = 'div.ss_book_box'

ala_name_lnk = 'a.bo3'
#ala_lnk = 'a.bo3'
ala_img = 'img.i_cover'
ala_price = 'ss_p2'


kyo_selectors = [
    'ul.prod_list div.horizontal'
]

yes_detail_selectors =[
    '*.bgYUI',
    'span.yPoint',
    'span.iconC',
    'em.yes_b',
    'span.authPub',
]

ala_remove_selectors = [
    'span.ss_p',

]

kyo_remove_selectors = [
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

def clean_content_extract2(url):

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    extracted_texts = []

    if "yes24.com" in url:
        selector = yes_selector
        name_select = yes_name
        price_select = yes_price
        lnk_select = yes_lnk

        name ="N/A"
        price = "N/A"
        link = "N/A"
        img = "N/A"

        for element in soup.select(selector):
            # 내부에서 제거할 태그 처리
            name_tag = element.select_one(name_select)
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'

            price_tag = element.select_one(price_select)
            price = price_tag.get_text(strip=True) if price_tag else 'N/A'

            lnk = 'https://www.yes24.com' + element.select_one(lnk_select).get("href")
            #이미지가 안나와서 상세페이지에서 이미지 추출해야함
            response_datail = requests.get(lnk)
            soup_detail = BeautifulSoup(response_datail.text, 'html.parser')


            img_tag = soup_detail.select_one(yes_img)
            img = img_tag.get("src") if img_tag else 'N/A'
            extracted_texts.append(f"{name} \n {price}\n{lnk} \n {img}")


    elif "aladin.co.kr" in url:
        selector = ala_selector
        name_lnk_select = ala_name_lnk
        price_select = ala_price
        img_select = ala_img

        for element in soup.select(selector):
            # 내부에서 제거할 태그 처리
            name_link_tag = element.select_one(name_lnk_select)
            name = name_link_tag.get_text(strip=True) if name_link_tag else 'N/A'

            price_tag = element.select_one(price_select)
            price = price_tag.get_text(strip=True) if price_tag else 'N/A'

            lnk = name_link_tag.get("href") if name_link_tag else "N/A"

            img = element.select_one(img_select)

            extracted_texts.append(f"{name} \n {price}\n{lnk} \n {img}")


    
    return '\n'.join(extracted_texts)


# 사용 예시
url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=DVD&SearchWord=Toy%20Story%20%281995%29%20blu%20ray'

# 추출하고 싶은 태그/클래스/ID 지정

extracted_text = clean_content_extract2(url)

with open("extracted_example.txt", "w", encoding="utf-8") as f:
    f.write(extracted_text)

print("선택한 태그의 텍스트가 파일에 저장되었습니다.")
