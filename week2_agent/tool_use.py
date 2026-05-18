"""
Step 3: Tool Use — 한 턴만, 수동으로 function_call 처리 (루프는 Step 4 에서).

학습 목표:
  - LLM 응답이 텍스트가 아닌 "function_call" 일 수 있다는 것을 본다
  - 그 호출 요청을 우리 코드가 실제로 실행해서 결과를 다시 돌려준다
  - = 콜센터 비유: 상담원(LLM)이 시스템(우리 코드)에 조회 요청 → 결과 수신 → 답변

실행:
  python tool_use.py
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"


# === 셋업: 실제 Python 함수 + LLM 이 볼 스키마 ===
def get_weather(city: str) -> str:
    return f"{city}는 맑음, 22도"


weather_declaration = {
    "name": "get_weather",
    "description": "주어진 도시의 현재 날씨를 반환한다",
    "parameters": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "도시 이름 (예: 서울)"},
        },
        "required": ["city"],
    },
}

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[weather_declaration])]
)


# === 1단계: 사용자 질문 → LLM ===
user_question = "오늘 서울 날씨 어때?"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}")

resp = client.models.generate_content(model=MODEL, contents=history, config=config)


# === 2단계: LLM 이 텍스트가 아닌 function_call 을 돌려줌 ===
function_call = resp.candidates[0].content.parts[0].function_call
print(f"\n[LLM 도구 요청] {function_call.name}(args={dict(function_call.args)})")


# === 3단계: 우리 코드가 실제로 실행 ===
# TODO (1): LLM 이 요청한 함수를 실제로 호출하세요.
#   function_call.name 은 "get_weather", function_call.args 는 {"city": "서울"} 같은 dict.
#   힌트: get_weather(**function_call.args)
result = ___
print(f"[실행 결과] {result}")


# === 4단계: 결과를 history 에 누적 → LLM 재호출 → 자연어 답변 ===
history.append(resp.candidates[0].content)

# TODO (2): 도구 실행 결과를 history 에 추가하세요.
#   형식: {"role": "user", "parts": [{"function_response": {"name": <함수명>, "response": {"result": <결과>}}}]}
history.append(___)

resp2 = client.models.generate_content(model=MODEL, contents=history, config=config)
print(f"\nModel: {resp2.text}")
