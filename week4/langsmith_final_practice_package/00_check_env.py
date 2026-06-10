import os
import importlib.util
from dotenv import load_dotenv

load_dotenv()

packages = [
    ("langsmith", "langsmith"),
    ("langchain", "langchain"),
    ("langchain_core", "langchain_core"),
    ("langchain_community", "langchain_community"),
    ("langchain_ollama", "langchain_ollama"),
    ("langchain_chroma", "langchain_chroma"),
    ("chromadb", "chromadb"),
    ("dotenv", "dotenv"),
    ("requests", "requests"),
]

print("=" * 70)
print("패키지 설치 확인")
print("=" * 70)

missing = []
for package_name, import_name in packages:
    if importlib.util.find_spec(import_name) is None:
        print(f"[없음] {package_name}")
        missing.append(package_name)
    else:
        print(f"[설치됨] {package_name}")

print("\n" + "=" * 70)
print(".env 설정 확인")
print("=" * 70)

for key in ["LANGSMITH_TRACING", "LANGSMITH_ENDPOINT", "LANGSMITH_API_KEY", "LANGSMITH_PROJECT", "OLLAMA_MODEL", "OLLAMA_EMBED_MODEL"]:
    value = os.getenv(key)
    if key == "LANGSMITH_API_KEY" and value:
        value = value[:8] + "..." + value[-4:]
    print(f"{key} = {value}")

if missing:
    print("\n누락된 패키지가 있습니다. pip install -r requirements.txt 를 실행하세요.")
elif not os.getenv("LANGSMITH_API_KEY") or "여기에" in os.getenv("LANGSMITH_API_KEY", ""):
    print("\n주의: LANGSMITH_API_KEY가 아직 설정되지 않았습니다.")
else:
    print("\nLangSmith 실습 준비가 완료되었습니다.")
