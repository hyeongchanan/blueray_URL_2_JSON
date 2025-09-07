import json
import os
from clean_content_extract import clean_content_extract
from openAiApi import summarize_text

INPUT_FILE = "search_links.json"
OUTPUT_FILE = "blueray_summary2.json"

# 기존 저장된 결과 불러오기 (있으면 이어서)
if os.path.exists(OUTPUT_FILE):
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        final_results = json.load(f)
else:
    final_results = {}

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    url_data = json.load(f)

global_id = 1
processed_count = 0

for movie_key, urls in url_data.items():
    if movie_key not in final_results:
        final_results[movie_key] = {}

    for site_name, url in urls.items():
        # 이미 처리된 경우 skip
        if site_name in final_results[movie_key]:
            continue

        print(f"Processing {movie_key} - {site_name} ...")
        try:
            text = clean_content_extract(url)
            if not text.strip(): 
                print(f"⚠️ 검색 결과 없음 null: {movie_key} - {site_name}, 건너뜀")
                final_results[movie_key][site_name] = None
                continue    
            summary = summarize_text(text)

            try:
                summary_json = json.loads(summary)
                if isinstance(summary_json, dict):
                    summary_json = [summary_json]
                summary_json = [obj for obj in summary_json if obj is not None]

    # 전부 None이면 스킵
                if not summary_json:
                    print(f"⚠️ 요약 결과가 null: {movie_key} - {site_name}, 건너뜀")
                    final_results[movie_key][site_name] = None
                    continue    
                summary_with_id = []
                for obj in summary_json:
                    obj["id"] = global_id
                    global_id += 1
                    summary_with_id.append(obj)

                final_results[movie_key][site_name] = summary_with_id

            except json.JSONDecodeError:
                print(f"⚠️ JSON 파싱 실패: {movie_key} - {site_name}")
                final_results[movie_key][site_name] = None

        except Exception as e:
            print(f"⚠️ 처리 실패: {movie_key} - {site_name} -> {e}")
            final_results[movie_key][site_name] = None

        processed_count += 1

        # 5개마다 저장
        if processed_count % 3 == 0:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(final_results, f, ensure_ascii=False, indent=2)
            print(f"💾 {processed_count}개 처리 완료, 중간 저장됨.")

# 마지막 저장
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(final_results, f, ensure_ascii=False, indent=2)

print("✅ 모든 URL 처리 완료, blueray_summary.json에 저장되었습니다.")
