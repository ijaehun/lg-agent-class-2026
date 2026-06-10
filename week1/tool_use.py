"""Step 3: Tool Use — LLM 에 도구 호출 권한 주기 (베이스라인).

도구 호출 4단계:
  1. LLM 호출 시 도구 선언 (declaration) 등록
  2. LLM 응답이 텍스트 대신 function_call 반환
  3. 우리 코드가 실제 함수 실행
  4. 결과를 function_response 로 LLM 에 돌려줌 → LLM 이 자연어 답
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
NOTES_DIR = Path(__file__).parent / "notes"


# === [1] 도구 함수 — 그냥 일반 Python 함수 ===
# LLM 이 직접 실행하지 못함. 우리 코드가 실행하고 결과만 LLM 에게 전달.
def read_note(filename: str) -> str:
    """지정한 노트 파일의 내용을 읽어 반환."""
    path = NOTES_DIR / filename
    if not path.exists():
        return f"[오류] 파일 없음: {filename}"
    return path.read_text(encoding="utf-8")


# === [2] LLM 이 참조할 도구 명세 (declaration) ===
# - name        : 도구 이름 (LLM 이 부를 때 사용)
# - description : LLM 이 "이 도구를 언제 부를지" 판단하는 근거
# - parameters  : 도구의 입력 인자 스키마 (JSON Schema)
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

# LLM 호출 옵션에 도구 등록 — types.Tool 안에 여러 declaration 묶어서 전달
config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[read_note_declaration])]
)


# === 사용자 질문 — 답하려면 LLM 이 read_note 를 불러야 함 ===
user_question = "policy_leave.md 파일 내용을 한 줄로 요약해줘"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}")


# === [3] LLM 호출 → 응답에서 function_call 추출 ===
# 도구가 등록되어 있으면 LLM 이 텍스트 대신 "이 함수를 이렇게 부르세요" 라는
# function_call (structured 메시지) 을 반환할 수 있음.
resp = client.models.generate_content(model=MODEL, contents=history, config=config)
function_call = resp.candidates[0].content.parts[0].function_call
print(f"\n[LLM 도구 요청] {function_call.name}(args={dict(function_call.args)})")


# === [4-1] 우리 코드가 실제 함수 실행 ===
# **function_call.args 는 dict 언패킹 — filename="policy_leave.md" 로 전달됨
result = read_note(**function_call.args)
print(f"[실행 결과 (앞 100자)] {result[:100]}...")


# === [4-2] LLM 의 도구 요청 + 우리 측 결과를 history 에 누적 ===
# role="user" 인 이유: LLM 입장에서 외부 정보 (도구 결과) 는 user 메시지로 인식
history.append(resp.candidates[0].content)
history.append({
    "role": "user",
    "parts": [{
        "function_response": {
            "name": "read_note",
            "response": {"result": result},
        }
    }],
})


# === [4-3] 다시 LLM 호출 → 결과 보고 자연어로 답변 ===
resp2 = client.models.generate_content(model=MODEL, contents=history, config=config)
print(f"\nModel: {resp2.text}")
