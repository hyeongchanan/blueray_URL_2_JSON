



import openai
import os
from clean_content import clean_content
import json

openai.api_key = "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"
example_json = """
  {
    "id": 1,
    "name": "28년후",
    "resolution": "4K",
    "year": 2025,
    "price": 12000,
    "maker": "마블코믹스",
    "limited_edition": true
  },
  {
    "id": 2,
    "name": "토이스토리",
    "resolution": "4K Ultra HD + Blu-ray",
    "year": 1995,
    "price": 65000,
    "maker": "픽사",
    "limited_edition": false
  },
"""

def summarize_text(input_text, max_tokens=2000):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 웹 크롤링으로 얻은 텍스트를 정제해 JSON 파일을 만드는 생성기야."},
            {"role": "user", "content": f"""
            다음은 블루레이 상품들의 정보를 포함한 텍스트야.
            각 상품들을 예시의 형식과 정확히 동일한 형식으로 JSON 파일을 만들어줘. 예시는 아래와 같아:
            \n{example_json}
            만약 값을 찾지 못하면 N/A 로 표시해줘
            \n\n{input_text}
            """}
        ],
        temperature=0.3,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content


url = 'https://www.yes24.com/product/search?domain=ALL&query=Toy%20Story%20%281995%29'
input_text = clean_content(url)
summary = summarize_text(input_text)



# 'w' 모드는 파일을 새로 쓰거나 기존 내용을 덮어씀
with open("example.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print("파일에 텍스트가 저장되었습니다.")

# JSON 파싱 체크
try:
    data = json.loads(f"[{summary}]")  # 여러 객체일 때를 대비
    with open("example.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("JSON 파일 저장 완료")
except json.JSONDecodeError:
    print("GPT 출력이 JSON 형식이 아닙니다. 확인 필요")
