"""
Step 5: RAG = agent loop + 검색 도구 + grounding

학습 목표:
  - W2 의 agent_loop 골격은 그대로. 도구만 search_notes 로 추가/교체.
  - system_instruction 으로 "검색 결과에만 근거해 답하기" 강제 → 할루시네이션 방지
  - 즉 RAG = Retrieval (search_notes) + Augmented Generation (system_instruction)

실행:
  python rag.py
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


# === 도구 구현: 키워드 검색 ===
def search_notes(keyword: str) -> list[dict]:
    """notes/ 폴더에서 키워드와 매칭되는 파일들을 점수순으로 반환."""
    keywords = keyword.lower().split()
    results = []
    for path in NOTES_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8").lower()

        # TODO (1): 검색 점수 계산.
        #   생각해볼 거리: 실전 RAG 는 임베딩 + 벡터 DB 지만 본질은 같아요.
        #     "관련성 있는 문서를 골라 LLM 에 준다"
        #   keywords 중 몇 개가 text 안에 나오는지 카운트.
        #   힌트: score = sum(1 for kw in keywords if kw in text)
        score = ___

        if score > 0:
            preview = path.read_text(encoding="utf-8")[:200]
            results.append({"score": score, "filename": path.name, "preview": preview})
    results.sort(key=lambda x: -x["score"])
    return results[:3]


TOOL_FUNCTIONS = {
    "search_notes": search_notes,
}


# === LLM 이 보는 도구 스키마 ===
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
                "keyword": {
                    "type": "string",
                    "description": "검색 키워드 (예: '연차 신입', '재택')",
                },
            },
            "required": ["keyword"],
        },
    },
]


# === 시스템 프롬프트: grounding 강제 ===
# TODO (2): 시스템 프롬프트를 직접 작성해보세요.
#   생각해볼 거리: 이 프롬프트가 없으면 LLM 이 어떻게 답할까? (할루시네이션 위험)
#   포인트 두 가지:
#     ① search_notes 로 먼저 검색하라
#     ② 검색 결과에 없는 내용은 추측하지 말고 "문서에 없습니다" 라고 답하라
#   예시 (그대로 써도 되고, 본인 톤으로 바꿔도 됩니다):
#     "당신은 사내 노트를 검색해서 직원 질문에 답하는 도우미입니다. "
#     "정책·규정·회의록에 관한 질문은 반드시 search_notes 로 먼저 검색한 뒤, "
#     "검색 결과에 근거해서만 답하세요. "
#     "검색 결과에 없는 내용은 추측하지 말고 '문서에 없습니다' 라고 답하세요."
SYSTEM_INSTRUCTION = ___

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[types.Tool(function_declarations=tool_declarations)],
)


# === 사용자 질문 ===
user_question = "신입사원인데 연차 언제부터 쓸 수 있어?"
history = [{"role": "user", "parts": [{"text": user_question}]}]
print(f"You: {user_question}\n")


# === Agent Loop (agent_loop.py 와 동일 — 골격은 그대로) ===
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
