"""
Step 3: Tool Use — 한 턴만, 수동으로 function_call 처리 (루프는 Step 4 에서).

학습 목표:
  - LLM 응답이 텍스트가 아닌 "function_call" 일 수 있다는 것을 본다
  - 그 호출 요청을 우리 코드가 실제로 실행해서 결과를 다시 돌려준다
  - W1 의 한계 (LLM 이 내 노트를 모름) → 도구로 해결

실행:
  python tool_use.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"

NOTES_DIR = Path(__file__).parent.parent / "notes"


# === 도구 구현: 노트 파일 읽기 ===
def read_note(filename: str) -> str:
    """notes/ 폴더의 노트 파일 내용을 반환."""
    path = NOTES_DIR / filename
    if not path.exists():
        return f"[오류] 파일 없음: {filename}"
    return path.read_text(encoding="utf-8")


# === LLM 이 볼 도구 스키마 ===
read_note_declaration = {
    "name": "read_note",
    "description": (
        "notes/ 폴더에서 지정한 노트 파일의 내용을 읽어 반환한다. "
        "회사 정책·회의록·온보딩 등의 문서에 대한 질문에 사용."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "파일명 (예: policy_leave.md, meeting_2026-05-19.md)",
            },
        },
        "required": ["filename"],
    },
}

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[read_note_declaration])]
)


# === 1단계: 사용자 질문 → LLM ===
user_question = "policy_leave.md 파일 내용을 한 줄로 요약해줘"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}")

resp = client.models.generate_content(model=MODEL, contents=history, config=config)


# === 2단계: LLM 이 텍스트가 아닌 function_call 을 돌려줌 ===
function_call = resp.candidates[0].content.parts[0].function_call
print(f"\n[LLM 도구 요청] {function_call.name}(args={dict(function_call.args)})")


# === 3단계: 우리 코드가 실제로 실행 ===
# TODO (1): LLM 이 요청한 함수를 실제로 호출해보세요.
#   생각해볼 거리: 왜 * 한 개가 아니라 ** 두 개? (function_call.args 는 dict)
#   힌트: read_note(**function_call.args)
result = ___
print(f"[실행 결과 (앞 100자)] {result[:100]}...")


# === 4단계: 결과를 history 에 누적 → LLM 재호출 → 자연어 답변 ===
history.append(resp.candidates[0].content)

# TODO (2): 도구 실행 결과를 history 에 추가하세요.
#   생각해볼 거리: role 이 왜 'user' 일까? 도구 결과를 user 메시지로 취급하는 이유는?
#   형식: {"role": "user", "parts": [{"function_response": {"name": <함수명>, "response": {"result": <결과>}}}]}
history.append(___)

resp2 = client.models.generate_content(model=MODEL, contents=history, config=config)
print(f"\nModel: {resp2.text}")
