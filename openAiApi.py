import openai
from clean_content import clean_content


openai.api_key = "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"


def summarize_text(input_text, max_tokens=150):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "너는 웹 크롤링을 통해 추출한 텍스트 데이터를 한번더 정제해주는 추출기야"},
            {"role": "user", "content": f"""다음은 블루레이 상품을 검색한 웹페이지에서 추출한 정보야, 
                각 상품의 정보를 JSON 파일로 정리해줘  
             
             출력 예시:
             {{
            "Toy Story": [
                {
                "id": 1,
                "year" : 1995
                "price": 10000,
                "resolution": "4K",
                "maker": "픽사",
                "url": "https://www.dvd.co.kr/...",
                "limited_edition": true
                },
            }}
            \n{input_text}"""}
        ],
        temperature=0.3,
        max_tokens=max_tokens
    )
    return response["choices"][0]["message"]["content"]

# 예시 사용

url = 'https://www.yes24.com/product/search?domain=DVD&query=%25EB%25A6%25B4%25EB%25A1%259C%25EC%2599%2580%2520%25EC%258A%25A4%25ED%258B%25B0%25EC%25B9%2598%2520%25EB%25B8%2594%25EB%25A3%25A8%25EB%25A0%2588%25EC%259D%25B4'
input_text = clean_content(url)
summary = summarize_text(input_text)
print(summary)