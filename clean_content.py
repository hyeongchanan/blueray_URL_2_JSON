import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from parse_bluray_title import parse_bluray_title
import openai

openai.api_key = "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"
client = openai.OpenAI(api_key = openai.api_key)

# 사이트별 셀렉터
yes_selector = 'div.itemUnit'
yes_name = 'a.gd_name'
yes_lnk = 'a.lnk_img'
yes_img = 'img.gImg'
yes_price = 'em.yes_b'
yes_auth = 'span.info_auth'
yes_date = 'span.info_date'
yes_des = 'div.txt_des'

ala_selector = 'div.ss_book_box>table'
ala_name_lnk = 'a.bo3'
ala_img = 'img.i_cover'
ala_price = 'span.ss_p2'
ala_auth = 'div.ss_book_list>ul li:nth-of-type(2) a:last-of-type'
ala_date = 'div.ss_book_list>ul li:nth-of-type(2)'

kyo_selector = 'ul.prod_list div.horizontal'
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

def parse_bluray_titles_batch(titles):
    """배치 OpenAI API 호출"""
    prompt = f"""
Extract each Blu-ray title into JSON with the following keys:
- movie_name
- region_code (or "N/A")
- resolution (or "N/A")
- limited_edition (true/false)

Titles: {json.dumps(titles, ensure_ascii=False)}

Return a JSON array where each element corresponds to a title in order.
Return JSON only.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    result_str = response.choices[0].message.content.strip()
    return json.loads(result_str)

def clean_content_extract2(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    extracted_data = []

    if "yes24.com" in url:
        tasks = []

        
        if soup.select(yes_des):
            print("검색  결과가 없습니다")
            return None
        
        elements = soup.select(yes_selector)

        if elements == []:
            print("검색  결과가 없습니다")
            return None
        for element in elements:
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

        # 모든 제목을 모아서 배치 API 호출
        titles = [t[0] for t in tasks]
        bluray_infos = parse_bluray_titles_batch(titles)

        # 최종 데이터 조합
        for i, (task, bluray_info) in enumerate(zip(tasks, bluray_infos)):
            name_raw, price, lnk, auth, date = task
            item = {
                **bluray_info,
                "price": price,
                "link": lnk,
                "img": images[i] if i < len(images) else 'N/A',
                "auth": auth,
                "date": date
            }
            extracted_data.append(item)

        return extracted_data


    elif "aladin.co.kr" in url:
        tasks = []
        elements = soup.select(ala_selector)
        if elements == []:
            print("검색  결과가 없습니다")
            return None
        for element in elements:
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

            tasks.append((name, price, lnk, img, auth, date))
        

        # 모든 제목을 모아서 배치 API 호출
        titles = [t[0] for t in tasks]
        bluray_infos = parse_bluray_titles_batch(titles)

        # 최종 데이터 조합
        for i, (task, bluray_info) in enumerate(zip(tasks, bluray_infos)):
            name_raw, price, lnk, img, auth, date = task
            item = {
                **bluray_info,  # movie_name, region_code, resolution, limited_edition 포함
                "price": price,
                "link": lnk,
                "img": img,
                "auth": auth,
                "date": date
            }
            extracted_data.append(item)
        return extracted_data


    elif "kyobobook.co.kr" in url:
        elements = soup.select(kyo_selector)

        if elements == []:
            print("검색  결과가 없습니다")
            return None
        tasks = []
        
        for element in elements:
            price_tag = element.select_one(kyo_price)
            
            if not price_tag:
                continue
            price = price_tag.get_text(strip=True).replace("원", "").replace(",", "")
            name_tag = element.select_one(kyo_name)
            name = name_tag.get_text(strip=True) if name_tag else 'N/A'
            lnk_tag = element.select_one(kyo_lnk)
            lnk = lnk_tag.get("href") if lnk_tag else 'N/A'
            img_tag = element.select_one(kyo_img)
            img = img_tag.get("src") if img_tag else 'N/A'
            auth_tag = element.select_one(kyo_auth)
            auth = auth_tag.get_text(strip=True) if auth_tag else 'N/A'
            date = 'N/A'  # 날짜 정보가 없으면 N/A

            tasks.append((name, price, lnk, img, auth, date))

        # 모든 제목을 모아서 배치 API 호출
        titles = [t[0] for t in tasks]
        bluray_infos = parse_bluray_titles_batch(titles)
        # 최종 데이터 조합
        for i, (task, bluray_info) in enumerate(zip(tasks, bluray_infos)):
            name_raw, price, lnk, img, auth, date = task
            item = {
                **bluray_info,  # movie_name, region_code, resolution, limited_edition 포함
                "price": price,
                "link": lnk,
                "img": img,
                "auth": auth,
                "date": date
            }
            extracted_data.append(item)
        return extracted_data
    return extracted_data

# 사용 예시
"""
#url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=DVD&SearchWord=%EC%8A%A4%EC%A6%88%EB%A9%94+%EB%B8%94%EB%A3%A8%EB%A0%88%EC%9D%B4'
url = 'https://www.yes24.com/product/search?domain=DVD&query=Jacket%2C%20The%20%282005%29&page=1&size=24&dispNo2=004001052'
#url = 'https://search.kyobobook.co.kr/search?keyword=%EB%B8%94%EB%A3%A8%EB%A0%88%EC%9D%B4%20%E3%85%81%E3%84%B4%E3%85%87%E3%84%BB%E3%85%87%E3%84%BB%E3%84%B4%E3%84%B9%E3%85%87&gbCode=TOT&target=total'
extracted_data = clean_content_extract2(url)

# JSON 파일로 저장
with open("extracted_example2.json", "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=4)

print("데이터가 JSON 형식으로 저장되었습니다.")
"""