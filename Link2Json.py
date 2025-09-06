import json
from clean_content import clean_content
from openAiApi import summarize_text

with open("link_test.json", "r", encoding="utf-8") as f:
    url_data = json.load(f)

final_results = {}


for movie_key, urls in url_data.items():
    final_results[movie_key] = {}
    for site_name, url in urls.items():
        print(f"Processing {movie_key} - {site_name} ...")
        try:
            text = clean_content(url)
            summary = summarize_text(text)
            # GPT가 반환한 문자열을 JSON으로 변환 시도
            try:
                summary_json = json.loads(f"[{summary}]")  # 여러 객체일 수 있어서 배열로 감쌈
                final_results[movie_key][site_name] = summary_json
            except json.JSONDecodeError:
                print(f"⚠️ JSON 파싱 실패: {movie_key} - {site_name}")
                final_results[movie_key][site_name] = None
        except Exception as e:
            print(f"⚠️ 처리 실패: {movie_key} - {site_name} -> {e}")
            final_results[movie_key][site_name] = None

# 결과를 JSON 파일로 저장
with open("blueray_summary.json", "w", encoding="utf-8") as f:
    json.dump(final_results, f, ensure_ascii=False, indent=2)

print("✅ 모든 URL 처리 완료, blueray_summary.json에 저장되었습니다.")