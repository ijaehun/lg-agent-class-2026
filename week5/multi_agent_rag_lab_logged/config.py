"""
수업용 설정 파일
- 코딩 경험이 적은 수강생도 여기의 값만 바꾸면 실행 흐름을 조정할 수 있도록 구성
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REFERENCE_DIR = DATA_DIR / "reference"
LOG_DIR = DATA_DIR / "logs"
VECTOR_STORE_DIR = BASE_DIR / "vector_store"
OUTPUT_DIR = BASE_DIR / "outputs"

# Ollama 모델명
# 사전 설치 예시:
#   ollama pull llama3.1:8b
#   ollama pull nomic-embed-text
CHAT_MODEL = "llama3.1:8b"
EMBED_MODEL = "nomic-embed-text"

# True로 바꾸면 Ollama 없이도 전체 workflow의 모양을 확인할 수 있음
USE_MOCK_LLM = False

# 검색 결과 개수
TOP_K = 4
