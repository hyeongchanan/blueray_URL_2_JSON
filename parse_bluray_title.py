import openai

openai.api_key = "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"

client = openai.OpenAI(api_key = openai.api_key)  # 1.x 이상에서는 이렇게 client 생성

def parse_bluray_title(title: str) -> str:
    prompt = f"""
Extract from the Blu-ray title into JSON:
- movie_name
- region_code (or "N/A")
- resolution (or "N/A")
- limited_edition (true/false)

Title: "{title}"

Return JSON only.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content.strip()

# 테스트
if __name__ == "__main__":
    bluray_title = "Jumanji (1995) (쥬만지)(지역코드1)(DVD) "
    result_json = parse_bluray_title(bluray_title)
    print(result_json)