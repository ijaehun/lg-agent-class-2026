"""
Step 4: Agent Loop — LLM 이 텍스트로 답할 때까지 도구 호출을 while 로 반복.

학습 목표:
  - tool_use.py 는 "한 턴" 만 처리했다. 실제 에이전트는 도구 결과를 보고
    또 다른 도구를 부를 수 있다 → 루프가 필요하다.
  - 종료 조건: LLM 이 더 이상 function_call 을 안 만들고 텍스트로 답할 때.
  - 안전장치: MAX_TURNS — LLM 이 도구를 멈추지 않을 때를 대비.

★ 이 파일이 곧 "에이전트의 골격" 입니다. LangChain · CrewAI 도 결국 이걸 감싼 것.

실행:
  python agent_loop.py
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
MAX_TURNS = 5


# === 도구 실제 구현 ===
def get_weather(city: str) -> dict:
    data = {
        "서울": {"condition": "맑음", "temp_celsius": 22},
        "부산": {"condition": "흐림", "temp_celsius": 25},
        "제주": {"condition": "비",   "temp_celsius": 18},
    }
    return data.get(city, {"condition": "알 수 없음", "temp_celsius": 0})


def recommend_outfit(temp_celsius: int) -> str:
    if temp_celsius >= 25:
        return "반팔 + 반바지"
    elif temp_celsius >= 15:
        return "긴팔 + 청바지"
    else:
        return "패딩 + 목도리"


# === LLM 이 부른 이름을 실제 함수로 라우팅 ===
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "recommend_outfit": recommend_outfit,
}


# === LLM 이 보는 도구 스키마 ===
tool_declarations = [
    {
        "name": "get_weather",
        "description": "주어진 도시의 현재 날씨와 기온(섭씨)을 반환한다",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "도시 이름 (예: 서울)"},
            },
            "required": ["city"],
        },
    },
    {
        "name": "recommend_outfit",
        "description": "현재 기온(섭씨)에 따라 적절한 옷차림을 추천한다",
        "parameters": {
            "type": "object",
            "properties": {
                "temp_celsius": {"type": "integer", "description": "현재 기온 (섭씨)"},
            },
            "required": ["temp_celsius"],
        },
    },
]

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=tool_declarations)]
)


# === 사용자 질문 ===
user_question = "서울 날씨 보고 오늘 뭐 입을지 추천해줘"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}\n")


# === Agent Loop ===
for turn in range(1, MAX_TURNS + 1):
    print(f"--- turn {turn} ---")
    resp = client.models.generate_content(model=MODEL, contents=history, config=config)
    content = resp.candidates[0].content

    # function_call 이 들어있는 part 들만 추리기
    function_calls = [p.function_call for p in content.parts if p.function_call]

    # TODO (1): 종료 조건을 채우세요.
    #   생각해볼 거리: 이 break 가 없으면 어떻게 될까? (무한 루프? MAX_TURNS 도달?)
    #   function_calls 가 비어있으면 = LLM 이 자연어로 답한 상태 → 출력하고 break.
    #   힌트:
    #     if not function_calls:
    #         print(f"\nModel: {resp.text}")
    #         break
    ___

    # LLM 의 도구 요청 메시지를 history 에 그대로 누적
    history.append(content)

    # 요청된 도구들을 모두 실행하고 결과 part 들을 모아 한 메시지로 누적
    tool_response_parts = []
    for fc in function_calls:
        print(f"[도구 요청] {fc.name}({dict(fc.args)})")

        # TODO (2): 이름(fc.name) 으로 실제 함수를 라우팅해서 호출하세요.
        #   생각해볼 거리: 도구가 100개라면? 딕셔너리 라우팅이 if/elif 보다 나은 이유.
        #   힌트: TOOL_FUNCTIONS 딕셔너리를 사용. result = TOOL_FUNCTIONS[fc.name](**fc.args)
        result = ___

        print(f"[결과]      {result}")
        tool_response_parts.append({
            "function_response": {
                "name": fc.name,
                "response": {"result": result},
            }
        })
    history.append({"role": "user", "parts": tool_response_parts})
else:
    # for 루프가 break 없이 끝난 경우 = MAX_TURNS 도달
    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과 — LLM 이 도구 호출을 멈추지 않음")
