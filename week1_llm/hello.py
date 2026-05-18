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

# TODO (1): 강사가 알려주는 모델명과 프롬프트를 채우세요.
response = client.models.generate_content(
    model="___",       # 예: "gemini-2.5-flash"
    contents="___",    # 예: "안녕? 한 줄로 자기소개 해줘"
)

print(response.text)
