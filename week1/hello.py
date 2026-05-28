"""
Step 1: 가장 단순한 LLM 호출 — 베이스라인.

학습 목표:
  - genai.Client 로 Gemini 에 연결한다
  - client.models.generate_content() 한 번 호출해서 응답을 받는다
  - 응답에서 텍스트를 꺼내 출력한다

실행:
  python hello.py
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# 1. 클라이언트 생성 (API 키로 인증)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 2. ★ LLM 호출 — 핵심 한 줄
response = client.models.generate_content(
    model="gemini-2.5-flash",       # 사용할 모델
    contents="안녕? 한 줄로 자기소개 해줘",   # LLM 에 보낼 프롬프트
)

# 3. 응답에서 텍스트 추출
print(response.text)
