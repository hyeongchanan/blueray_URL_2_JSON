import json
import time
import re

from clean_content import clean_content
from URL2json import summarize_text, extract_json_from_text

import json
import time

def summarize_urls(movie_urls_dict, output_file="result.json"):
    final_results = []

    for movie_key, sites in movie_urls_dict.items():
        movie_result = {}
        movie_result["title"] = movie_key.split("::")[1]  # "1::Toy Story (1995)" -> "Toy Story (1995)"
        movie_result["sources"] = {}

        for site_name, url in sites.items():
            try:
                # URL에서 텍스트를 추출하고 요약(JSON) 생성
                clean_contents = clean_content(url)
                summarized = summarize_text(clean_contents)
                # 문자열로 나온 JSON을 파이썬 객체로 변환
                movie_result["sources"][site_name] = json.loads(summarized)
                time.sleep(1)  # API 과부하 방지
            except Exception as e:
                print(f"오류 발생: {url} -> {e}")
                movie_result["sources"][site_name] = None

        final_results.append(movie_result)

    # 최종 결과를 JSON 파일로 저장
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    return final_results

summarize_urls('link_t.json')