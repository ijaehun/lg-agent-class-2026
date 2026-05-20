"""
Step 2: 멀티턴 챗봇 (history 누적)

핵심 — LLM 은 stateless. 우리가 history 를 누적해서 매 호출마다 통째로 전송.

실행:
  python chat.py
  (대화 종료: 빈 줄 또는 "exit")
"""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"

# 대화 기록 리스트 — LLM 의 "기억"
history = []

while True:
    user = input("You: ").strip()
    if user == "" or user.lower() == "exit":
        break

    # 1. 사용자 발화 → history (role="user")
    history.append({"role": "user", "parts": [{"text": user}]})

    # 2. LLM 호출 — history 전체 전달 (매번 통째로 보내야 맥락 유지)
    resp = client.models.generate_content(model=MODEL, contents=history)
    print("Model:", resp.text)

    # 3. LLM 응답도 history 에 누적 (role="model")
    history.append({"role": "model", "parts": [{"text": resp.text}]})
