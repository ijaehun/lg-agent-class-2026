"""
Step 1: 가장 단순한 LLM 호출

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

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# TODO (1): 모델명과 프롬프트를 채워보세요.
#   생각해볼 거리:
#     - 처음엔 간단한 질문으로 ("안녕? 한 줄로 자기소개 해줘")
#     - 동작 확인되면 contents 를 바꿔서 시도해보세요:
#       "이번 주 우리 팀 회의록을 한 줄로 요약해줘"
#     - LLM 이 회의록 내용을 알까요? 모를까요? → 다음 주에 해결합니다 (도구로)
response = client.models.generate_content(
    model="___",       # 예: "gemini-2.5-flash"
    contents="___",    # 예: "안녕? 한 줄로 자기소개 해줘"
)

print(response.text)
