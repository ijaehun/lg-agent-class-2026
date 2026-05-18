"""
Step 2: 멀티턴 챗봇 (history 누적)

학습 목표:
  - hello.py 와의 차이 = 매 턴을 history 리스트에 쌓아서 통째로 보낸다
  - history 가 없으면 LLM 은 직전 대화를 기억하지 못한다 (=stateless)

실행:
  python chat.py
  (대화 종료: 빈 줄 또는 "exit")
"""

from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

history = []


def main():
    while True:
        user = input("You: ").strip()
        if user == "" or user.lower() == "exit":
            break

        # TODO (1): user 입력을 history 에 추가하세요.
        #   힌트: history.append({"role": "user", "parts": [{"text": ...}]})
        ___

        resp = client.models.generate_content(model=MODEL, contents=history)
        text = resp.text
        print("Model:", text)

        # TODO (2): 모델 응답도 history 에 추가하세요.
        #   힌트: role 은 "model".
        ___


if __name__ == "__main__":
    main()
