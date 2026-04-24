import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 설정
VAULT_PATH = r"C:\Users\UserK\Desktop\test-connet\\" # 성용님의 경로

class WikiHandler(FileSystemEventHandler):
    def on_created(self, event):
        # 새로운 .txt 파일이 생성되면 실행
        if not event.is_directory and event.src_path.endswith(".txt"):
            print(f"✨ 새 텍스트 파일 감지: {event.src_path}")
            self.convert_to_wiki(event.src_path)

    def convert_to_wiki(self, txt_path):
        # 1. 파일 읽기
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        title = os.path.basename(txt_path).replace(".txt", "")
        md_file_name = f"{title}.md"
        md_path = os.path.join(VAULT_PATH, md_file_name)

        # 2. 위키 구조화 (파일 1의 로직)
        wiki_content = f"""---
title: {title}
created: {time.strftime('%Y-%m-%d %H:%M:%S')}
tags: #auto_conversion #wiki
---
# {title}
{content}

---
## 🔗 연결된 지식
- [[hello]]
"""
        # 3. .md 파일로 저장
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(wiki_content)
        
        # 4. 원본 .txt 삭제 (선택 사항)
        os.remove(txt_path)
        
        # 5. 깃허브 동기화 (파일 2의 로직)
        self.sync_github(md_file_name)

    def sync_github(self, file_name):
        try:
            os.chdir(VAULT_PATH)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Auto-convert: {file_name}"], check=True)
            subprocess.run(["git", "push"], check=True)
            print(f"🚀 {file_name} 깃허브 동기화 완료!")
        except Exception as e:
            print(f"❌ 동기화 에러: {e}")

if __name__ == "__main__":
    event_handler = WikiHandler()
    observer = Observer()
    observer.schedule(event_handler, VAULT_PATH, recursive=False)
    observer.start()
    print(f"🔍 {VAULT_PATH} 폴더 감시 중... (Ctrl+C로 종료)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()