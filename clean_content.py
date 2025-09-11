import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

# 사이트별 셀렉터
yes_selector = 'div.itemUnit'
yes_name = 'a.gd_name'
yes_lnk = 'a.lnk_img'
yes_img = 'img.gImg'
yes_price = 'em.yes_b'
yes_auth = 'span.info_auth'
yes_date = 'span.info_date'

ala_selector = 'div.ss_book_box>table'
ala_name_lnk = 'a.bo3'
ala_img = 'img.i_cover'
ala_price = 'span.ss_p2'
ala_auth = 'div.ss_book_list>ul li:nth-of-type(2) a:last-of-type'
ala_date = 'div.ss_book_list>ul li:nth-of-type(2)'

kyo_selector = 'div.prod_area'
kyo_name = 'div.auto_overflow_inner span:nth-of-type(2)'
kyo_lnk = 'a.prod_link'
kyo_img = 'span.img_box img'
kyo_price = 'span.val'
kyo_auth = 'a.text'

def fetch_image(link):
    """상세페이지에서 이미지 가져오기"""
    try:
        response_detail = requests.get(link, timeout=5)
        soup_detail = BeautifulSoup(response_detail.text, 'html.parser')
        img_tag = soup_detail.select_one(yes_img)
        return img_tag.get("src") if img_tag else 'N/A'
    except:
        return 'N/A'

def clean_content_extract2(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    extracted_data = []

    if "yes24.com" in url:
        tasks = []
        for element in soup.select(yes_selector):
            price_tag = element.select_one(yes_price)
            if not price_tag:
                continue
            
            price = price_tag.get_text(strip=True).replace("원", "").replace(",", "")
            name_tag = element.select_one(yes_name)
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'
            lnk_tag = element.select_one(yes_lnk)
            lnk = 'https://www.yes24.com' + lnk_tag.get("href") if lnk_tag else 'N/A'
            auth_tag = element.select_one(yes_auth)
            auth = auth_tag.get_text(strip=True) if auth_tag else 'N/A'
            date_tag = element.select_one(yes_date)
            date = date_tag.get_text(strip=True) if date_tag else 'N/A'

            tasks.append((name, price, lnk, auth, date))

        # 병렬로 이미지 가져오기
        with ThreadPoolExecutor(max_workers=10) as executor:
            links = [task[2] for task in tasks]
            images = list(executor.map(fetch_image, links))

        # 최종 데이터 조합
        for i, (name, price, lnk, auth, date) in enumerate(tasks):
            extracted_data.append({
                "name": name,
                "price": price,
                "link": lnk,
                "img": images[i],
                "auth": auth,
                "date": date
            })

    elif "aladin.co.kr" in url:
        for element in soup.select(ala_selector):
            price_tag = element.select_one(ala_price)
            if not price_tag:
                continue
            price = price_tag.get_text(strip=True).replace("원", "").replace(",", "")
            name_link_tag = element.select_one(ala_name_lnk)
            name = name_link_tag.get_text(strip=True) if name_link_tag else 'N/A'
            lnk = name_link_tag.get("href") if name_link_tag else "N/A"
            img_tag = element.select_one(ala_img)
            img = img_tag.get("src") if img_tag else 'N/A'

            # auth와 date 분리
            date_tag = element.select_one(ala_date)
            auth_date = date_tag.get_text(strip=True) if date_tag else 'N/A'
            parts = [p.strip() for p in auth_date.split("|")]
            auth = parts[-2] if len(parts) >= 2 else 'N/A'
            date = parts[-1] if len(parts) >= 1 else 'N/A'

            extracted_data.append({
                "name": name,
                "price": price,
                "link": lnk,
                "img": img,
                "auth": auth,
                "date": date
            })

    elif "kyobobook.co.kr" in url:
        for element in soup.select(kyo_selector):
            price_tag = element.select_one(kyo_price)
            if not price_tag:
                continue
            price = price_tag.get_text(strip=True).replace("원", "").replace(",", "")
            name_tag = element.select_one(kyo_name)
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'
            lnk_tag = element.select_one(kyo_lnk)
            lnk = lnk_tag.get("href") if lnk_tag else "N/A"
            img_tag = element.select_one(kyo_img)
            img = img_tag.get("src") if img_tag else 'N/A'
            auth_tag = element.select_one(kyo_auth)
            auth = auth_tag.get_text(strip=True) if auth_tag else 'N/A'
            date = 'N/A'  # 교보는 날짜 정보가 없으면 N/A

            extracted_data.append({
                "name": name,
                "price": price,
                "link": lnk,
                "img": img,
                "auth": auth,
                "date": date
            })

    return extracted_data

# 사용 예시

#url = 'https://search.kyobobook.co.kr/search?keyword=Jumanji&target=total&totalType=hottracks&gbCode=TOT&cat2=%EC%9D%8C%EB%B0%98%2FDVD%40HOTTRACKS%40%40BLU-RAY%40BLURAY&cname=Jumanji'
url = 'https://www.yes24.com/product/search?domain=ALL&query=Toy%20Story%20%281995%29%20blu%20ray'
#url = 'https://search.kyobobook.co.kr/search?keyword=Toy%20Story&gbCode=TOT&target=total'
extracted_data = clean_content_extract2(url)

# JSON 파일로 저장
with open("extracted_example.json", "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=4)

print("데이터가 JSON 형식으로 저장되었습니다.")
