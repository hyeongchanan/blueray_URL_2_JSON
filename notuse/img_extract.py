import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 예스24 검색 결과 URL
url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=DVD&SearchWord=Sabrina&CategorySearch=&chkKeyTitle=on&SearchFieldEnable='

# HTTP 요청 헤더 설정 (User-Agent를 설정하여 봇 차단 우회)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 요청 보내기
response = requests.get(url, headers=headers)
response.raise_for_status()  # 요청 실패 시 예외 발생

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 이미지 저장 폴더 생성
os.makedirs('toy_story_images', exist_ok=True)

# 이미지 태그 찾기
img_tags = soup.find_all('img')

# 이미지 다운로드
for img in img_tags:
    img_url = img.get('src')
    if img_url:
        # 상대 경로를 절대 경로로 변환
        img_url = urljoin(url, img_url)
        # 이미지 파일 이름 설정
        img_name = os.path.join('toy_story_images', os.path.basename(img_url))
        try:
            # 이미지 다운로드
            img_data = requests.get(img_url).content
            with open(img_name, 'wb') as f:
                f.write(img_data)
            print(f'이미지 저장 완료: {img_name}')
        except Exception as e:
            print(f'이미지 다운로드 실패: {img_url}, 오류: {e}')
