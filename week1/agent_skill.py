"""Step 5: Skill 추가 — agent_loop 위에 search_notes 도구 한 개 더 (베이스라인).

핵심:
  - agent_loop 골격 그대로 + search_notes 도구만 추가
  - Agent loop 본문은 한 줄도 안 건드림
  - 결과: "신입사원 연차 정책 알려줘" → 검색 → 읽기 → 답변
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


# === 기존 도구 (agent_loop 와 동일) ===
def list_notes() -> list[str]:
    return sorted(p.name for p in NOTES_DIR.glob("*.md"))


def read_note(filename: str) -> str:
    path = NOTES_DIR / filename
    if not path.exists():
        return f"[오류] 파일 없음: {filename}"
    return path.read_text(encoding="utf-8")


# === ★ 새 도구: 키워드로 노트 검색 ===
def search_notes(keyword: str) -> list[str]:
    """notes/ 폴더의 .md 파일 중 keyword 가 포함된 파일명 리스트 반환."""
    results = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        if keyword in path.read_text(encoding="utf-8"):
            results.append(path.name)
    return results


# === 도구 라우팅 — search_notes 추가 (← 추가) ===
TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
    "search_notes": search_notes,
}

# === LLM 이 참조할 도구 명세 — search_notes declaration 추가 ===
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
    {
        "name": "search_notes",
        "description": "notes/ 폴더의 노트들에서 keyword 가 포함된 파일을 찾아 파일명 리스트를 반환한다. 파일명을 모르고 키워드만 알 때 사용 (예: '연차', '출장', '신입').",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {
                    "type": "string",
                    "description": "노트 내용에서 찾을 키워드",
                },
            },
            "required": ["keyword"],
        },
    },
]

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=tool_declarations)]
)


# === 사용자 질문 ===
user_question = "신입사원인데 연차 언제부터 쓸 수 있어?"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}\n")


# === Agent Loop — agent_loop 와 100% 동일 (안 바뀜) ===
for turn in range(1, MAX_TURNS + 1):
    print(f"--- turn {turn} ---")
    resp = client.models.generate_content(model=MODEL, contents=history, config=config)
    content = resp.candidates[0].content
    function_calls = [p.function_call for p in content.parts if p.function_call]

    if not function_calls:
        print(f"\nModel: {resp.text}")
        break

    history.append(content)
    tool_response_parts = []
    for fc in function_calls:
        print(f"[도구 요청] {fc.name}({dict(fc.args)})")
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
    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과")
