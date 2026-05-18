"""
Step 4: Agent Loop — LLM 이 텍스트로 답할 때까지 도구 호출을 while 로 반복.

학습 목표:
  - tool_use.py 는 "한 턴" 만. 실제 에이전트는 도구 결과 보고 또 도구 부를 수 있다 → 루프 필요
  - 종료 조건: LLM 이 function_call 안 만들고 자연어로 답할 때
  - 안전장치: MAX_TURNS

★ 이 파일이 곧 "에이전트의 골격". LangChain · CrewAI 도 결국 이걸 감싼 것.

실행:
  python agent_loop.py
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

NOTES_DIR = Path(__file__).parent.parent / "notes"


# === 도구 구현: 노트 목록 + 노트 읽기 ===
def list_notes() -> list[str]:
    """notes/ 폴더의 .md 파일 목록을 반환."""
    return sorted(p.name for p in NOTES_DIR.glob("*.md"))


def read_note(filename: str) -> str:
    """notes/ 폴더의 노트 파일 내용을 반환."""
    path = NOTES_DIR / filename
    if not path.exists():
        return f"[오류] 파일 없음: {filename}"
    return path.read_text(encoding="utf-8")


# === LLM 이 부른 이름을 실제 함수로 라우팅 ===
TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
}


# === LLM 이 보는 도구 스키마 ===
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
        #   힌트: TOOL_FUNCTIONS 딕셔너리 사용. result = TOOL_FUNCTIONS[fc.name](**fc.args)
        result = ___

        # 결과가 길면 잘라서 출력
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
    # for 루프가 break 없이 끝난 경우 = MAX_TURNS 도달
    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과 — LLM 이 도구 호출을 멈추지 않음")
