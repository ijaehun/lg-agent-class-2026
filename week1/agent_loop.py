"""Step 4: Agent Loop — list_notes + read_note 두 도구 + while 루프 (베이스라인).

핵심:
  - tool_use.py 는 한 턴만. agent_loop 는 LLM 이 자연어 답할 때까지 반복.
  - 종료 조건: LLM 이 function_call 안 만들고 자연어로 답할 때
  - 안전장치: MAX_TURNS

★ 이 파일이 곧 "에이전트의 골격". LangChain · CrewAI 도 결국 이걸 감싼 것.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
MAX_TURNS = 5

NOTES_DIR = Path(__file__).parent / "notes"


# === 도구 함수 두 개 ===
def list_notes() -> list[str]:
    """notes/ 폴더의 .md 파일 목록을 반환."""
    return sorted(p.name for p in NOTES_DIR.glob("*.md"))


def read_note(filename: str) -> str:
    """지정한 노트 파일의 내용을 반환."""
    path = NOTES_DIR / filename
    if not path.exists():
        return f"[오류] 파일 없음: {filename}"
    return path.read_text(encoding="utf-8")


# === 도구 라우팅 — 이름 → 함수 ===
TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
}

# === LLM 이 참조할 도구 명세 ===
tool_declarations = [
    {
        "name": "list_notes",
        "description": "notes/ 폴더에 어떤 노트 파일들이 있는지 목록을 반환한다. 무엇이 있는지 둘러볼 때 먼저 사용.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "read_note",
        "description": "지정한 노트 파일의 전체 내용을 읽어 반환한다. 자세한 내용이 필요할 때.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "list_notes 가 반환한 파일명 중 하나 (예: policy_leave.md)",
                },
            },
            "required": ["filename"],
        },
    },
]

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=tool_declarations)]
)


# === 사용자 질문 ===
user_question = "내 노트에 무슨 회의록이 있어? 가장 최근 회의록 한 줄로 요약해줘"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}\n")


# === Agent Loop — 핵심 3가지: 반복 / 종료 조건 / 도구 라우팅 ===
for turn in range(1, MAX_TURNS + 1):
    print(f"--- turn {turn} ---")
    resp = client.models.generate_content(model=MODEL, contents=history, config=config)
    content = resp.candidates[0].content

    # 응답에서 function_call 추출
    function_calls = [p.function_call for p in content.parts if p.function_call]

    # ★ 종료 조건: LLM 이 도구 안 부르고 자연어로 답하면 종료
    if not function_calls:
        print(f"\nModel: {resp.text}")
        break

    # LLM 의 도구 요청 메시지를 history 에 누적
    history.append(content)

    # 도구 실행 + function_response 형식으로 결과 누적
    tool_response_parts = []
    for fc in function_calls:
        print(f"[도구 요청] {fc.name}({dict(fc.args)})")
        # ★ 도구 라우팅 (이름 → 함수)
        result = TOOL_FUNCTIONS[fc.name](**fc.args)
        preview = str(result).replace("\n", " ")[:100]
        print(f"[결과]      {preview}{'…' if len(str(result)) > 100 else ''}")
        tool_response_parts.append({
            "function_response": {
                "name": fc.name,
                "response": {"result": result},
            }
        })
    history.append({"role": "user", "parts": tool_response_parts})
else:
    # ★ 안전장치: MAX_TURNS 도달
    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과")
