"""Step 5: RAG = search_notes + system_instruction (베이스라인).

핵심:
  - agent_loop 골격은 그대로. 도구만 search_notes + system_instruction 추가.
  - RAG = Retrieval (search_notes) + Augmented Generation (system_instruction 으로 grounding)
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


# === 검색 도구 — keyword 매칭 + 점수순 정렬 ===
def search_notes(keyword: str) -> list[dict]:
    """notes/ 에서 keyword 매칭 + 점수순 상위 3개 반환."""
    keywords = keyword.lower().split()
    results = []
    for path in NOTES_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8").lower()
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            preview = path.read_text(encoding="utf-8")[:200]
            results.append({"score": score, "filename": path.name, "preview": preview})
    results.sort(key=lambda x: -x["score"])
    return results[:3]


TOOL_FUNCTIONS = {"search_notes": search_notes}

tool_declarations = [
    {
        "name": "search_notes",
        "description": (
            "notes/ 폴더에서 키워드로 관련 노트를 검색해 매칭 파일과 미리보기를 반환한다. "
            "회사 정책·회의록·온보딩 등 사내 문서에 대한 질문에 반드시 사용."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "검색 키워드 (예: '연차 신입', '재택')"},
            },
            "required": ["keyword"],
        },
    },
]

# === ★ 핵심: system_instruction — 할루시네이션 방지 (grounding) ===
SYSTEM_INSTRUCTION = (
    "당신은 사내 노트를 검색해서 직원 질문에 답하는 도우미입니다. "
    "정책·규정·회의록에 관한 질문은 반드시 search_notes 로 먼저 검색한 뒤, "
    "검색 결과에 근거해서만 답하세요. "
    "검색 결과에 없는 내용은 추측하지 말고 '문서에 없습니다' 라고 답하세요."
)

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[types.Tool(function_declarations=tool_declarations)],
)


user_question = "신입사원인데 연차 언제부터 쓸 수 있어?"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}\n")

# === Agent Loop — W1 agent_loop 와 동일 ===
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
        preview = str(result).replace("\n", " ")[:120]
        print(f"[결과]      {preview}{'…' if len(str(result)) > 120 else ''}")
        tool_response_parts.append({
            "function_response": {
                "name": fc.name,
                "response": {"result": result},
            }
        })
    history.append({"role": "user", "parts": tool_response_parts})
else:
    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과")
