import os
import subprocess
from datetime import datetime

# 1. 설정: 성용님의 폴더 경로
VAULT_PATH = r"C:\Users\UserK\Desktop\test-connet" # 폴더 경로를 확인해주세요.

def format_to_wiki(raw_title, raw_content):
    """
    [파일 1의 기능] 날것의 데이터를 위키 구조로 변환합니다.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 옵시디언 마크다운 형식으로 변환
    wiki_content = f"""---
title: {raw_title}
created: {now}
tags: #automation #ai_agent #knowledge
---

# {raw_title}

## 📝 핵심 요약
- 자동 생성된 지식 문서입니다.
- 생성 일시: {now}

## 📖 상세 내용
{raw_content}

---
## 🔗 연결된 지식
- [[hello]]
- [나의 깃허브 저장소](https://github.com/sungyong-art/test-connet)
"""
    return wiki_content

def save_and_sync(title, content):
    """
    [파일 2의 기능] 파일을 저장하고 깃허브로 자동 동기화합니다.
    """
    # 파일명 정제 및 저장
    file_name = f"{title.replace(' ', '_')}.md"
    full_path = os.path.join(VAULT_PATH, file_name)
    
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 파일 생성 완료: {full_path}")

    # 깃허브 자동 업로드 실행
    try:
        os.chdir(VAULT_PATH)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", f"Auto-update: {file_name}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 깃허브 업로드 성공!")
    except Exception as e:
        print(f"❌ 동기화 실패: {e}")

# --- 실행 예시 ---
if __name__ == "__main__":
    # 에이전트가 가져온 데이터라고 가정합니다.
    test_title = "AI 비즈니스 자동화 전략"
    test_raw_data = "이 내용은 에이전트가 수집한 방대한 지식의 원본 데이터입니다..."

    # 1단계: 구조화 (파일 1 로직)
    formatted_data = format_to_wiki(test_title, test_raw_data)
    
    # 2단계: 저장 및 동기화 (파일 2 로직)
    save_and_sync(test_title, formatted_data)