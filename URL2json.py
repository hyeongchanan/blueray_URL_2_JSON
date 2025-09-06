from openai import OpenAI
from clean_content import clean_content
import re
import json


client = OpenAI(
  api_key="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"
)

def summarize_text(input_text, max_tokens=150):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {
                "role": "system",
                "content": "너는 웹 크롤링을 통해 추출한 텍스트 데이터를 한번더 정제해주는 추출기야"
            },
            {
                "role": "user",
                "content": f"""다음은 블루레이 상품을 검색한 웹페이지에서 추출한 정보야, 
각 상품의 정보를 JSON 객체로 출력해줘, 다른 내용없이, 정확히 출력 예시와 동일하게 출력해줘 

출력 예시:

    {{
        "id": 1,
        "name": "28년후",
        "resolution": "4K",
        "year": 1995,
        "price": 10000,
        "maker": "픽사",
        "limited_edition": true
    }}


\n{input_text}
"""
            }
        ],
        max_tokens=max_tokens
    )
    used_tokens = completion.usage.total_tokens if hasattr(completion, "usage") else max_tokens
    return completion.choices[0].message.content, used_tokens


def extract_json_from_text(text):
    """
    텍스트 내에서 가장 먼저 나오는 JSON 배열([]) 또는 객체({})를 추출한다.
    """
    array_match = re.search(r'\[\s*{.*?}\s*\]', text, re.DOTALL)
    if array_match:
        return array_match.group()
    object_match = re.search(r'{.*}', text, re.DOTALL)
    if object_match:
        return object_match.group()
    return None


url = 'https://www.yes24.com/product/search?domain=ALL&query=Toy%20Story%20%281995%29'

# 1) 원본 텍스트 크롤링 및 정제
clean_contents = clean_content(url)

# 2) API 호출
pure_info, used_tokens = summarize_text(clean_contents)

# 3) 원본 API 응답 텍스트 저장
with open("info_raw.txt", "w", encoding="utf-8") as f:
    f.write(pure_info)

# 4) JSON 문자열 추출
json_str = extract_json_from_text(pure_info)

# 5) JSON 파싱 및 저장
if json_str:
    try:
        parsed_json = json.loads(json_str)
        with open("info.json", "w", encoding="utf-8") as f:
            json.dump(parsed_json, f, ensure_ascii=False, indent=2)
        print("✅ JSON 저장 성공")
    except json.JSONDecodeError as e:
        print("⚠️ JSON 파싱 실패:", e)
else:
    print("⚠️ JSON 객체를 텍스트에서 찾지 못했습니다.")