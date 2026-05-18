"""
Step 5b: 에이전트형 RAG — search_docs 도구를 가진 agent loop.

학습 목표:
  - agent_loop.py 와 골격은 똑같다 (★). 도구가 search_docs 로 바뀌었을 뿐.
  - + system_instruction 으로 "검색 결과에만 근거해 답하기" 를 강제 → 할루시네이션 방지.
  - 즉 RAG = Retrieval(search_docs) + Augmented Generation(system_instruction 으로 grounding).

실행:
  python rag.py
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
MAX_TURNS = 5


# === 사내 위키 모킹 (실전에서는 벡터스토어 / DB) ===
DOCS = [
    {
        "title": "연차 사용 정책",
        "content": (
            "정규직은 입사 1년 후부터 연차 15일을 사용할 수 있다. "
            "신입사원은 입사 후 6개월 동안 월 1일씩 부여받는다. "
            "미사용 연차는 다음 해로 최대 5일까지 이월 가능하다."
        ),
    },
    {
        "title": "재택근무 가이드",
        "content": (
            "주 2회까지 재택근무가 가능하다. 사전에 팀 리더 승인이 필요하며, "
            "재택일에도 09:00-18:00 코어 시간은 응답 가능해야 한다."
        ),
    },
    {
        "title": "출장비 정산",
        "content": (
            "국내 출장은 일비 5만원, 숙박비 실비(최대 10만원/박). "
            "해외는 지역별 차등. 영수증 첨부 필수, 출장 종료 후 7일 이내 정산."
        ),
    },
    {
        "title": "교육비 지원",
        "content": (
            "외부 교육·자격증 응시료는 연 100만원 한도로 지원. "
            "사전 신청 후 부서장 승인이 필요하며, 수료증 제출 시 정산된다."
        ),
    },
]


# === 도구 실제 구현 (단순 키워드 매칭) ===
def search_docs(query: str) -> list[dict]:
    """간단한 키워드 점수 검색 — 실전에서는 임베딩 + 벡터 DB."""
    keywords = query.lower().split()
    scored = []
    for doc in DOCS:
        text = (doc["title"] + " " + doc["content"]).lower()

        # TODO (1): 검색 점수 계산.
        #   keywords 중 몇 개가 text 안에 나오는지 카운트하세요.
        #   힌트: score = sum(1 for kw in keywords if kw in text)
        score = ___

        if score > 0:
            scored.append((score, doc))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [doc for _, doc in scored[:3]]


TOOL_FUNCTIONS = {
    "search_docs": search_docs,
}


# === LLM 이 보는 도구 스키마 ===
tool_declarations = [
    {
        "name": "search_docs",
        "description": (
            "사내 위키에서 키워드로 관련 문서를 검색한다. "
            "회사 정책·규정·복지 관련 질문에 반드시 사용."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "검색 키워드 (예: '연차 신입사원', '재택')",
                },
            },
            "required": ["query"],
        },
    },
]


# === 시스템 프롬프트: 에이전트의 역할 + 할루시네이션 방지 ===
# TODO (2): 시스템 프롬프트 작성.
#   포인트: ① search_docs 로 먼저 검색하라, ② 검색 결과에 없는 내용은 추측 금지.
#   힌트 (강사가 알려주는 예시를 그대로 입력해도 됩니다):
#     "당신은 회사 내부 위키를 검색해서 직원 질문에 답하는 도우미입니다. "
#     "정책·규정·복지에 관한 질문은 반드시 search_docs 로 먼저 검색한 뒤, "
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
        print(f"[결과]      {result}")
        tool_response_parts.append({
            "function_response": {
                "name": fc.name,
                "response": {"result": result},
            }
        })
    history.append({"role": "user", "parts": tool_response_parts})
else:
    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과")
