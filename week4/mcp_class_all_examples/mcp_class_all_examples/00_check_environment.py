# 00_check_environment.py
# 실습 환경이 준비되었는지 확인하는 파일입니다.

import importlib.util
import sys

packages = [
    ("fastmcp", "fastmcp"),
    ("requests", "requests"),
    ("python-dotenv", "dotenv"),
    ("pymupdf", "fitz"),
    ("sentence-transformers", "sentence_transformers"),
    ("chromadb", "chromadb"),
    ("pyautogui", "pyautogui"),
    ("pillow", "PIL"),
]

print("=" * 70)
print("Python 버전")
print("=" * 70)
print(sys.version)

print("\n" + "=" * 70)
print("패키지 설치 확인")
print("=" * 70)

missing = []

for package_name, import_name in packages:
    if importlib.util.find_spec(import_name) is None:
        print(f"[없음] {package_name}")
        missing.append(package_name)
    else:
        print(f"[설치됨] {package_name}")

if missing:
    print("\n설치되지 않은 패키지가 있습니다.")
    print("아래 명령어를 다시 실행하세요.")
    print("\npip install -r requirements.txt")
else:
    print("\n모든 필수 패키지가 설치되어 있습니다.")
