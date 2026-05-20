"""W2 Part 2: LangChain — rag.py 가 한 줄로 (베이스라인).

핵심:
  - rag.py 와 동일한 일을 LangChain (LangGraph) 의 create_react_agent 로
  - 도구 함수 본문은 그대로. @tool 데코레이터만 추가
  - LLM 호출 / while 루프 / function_call·response 처리 → 다 LangChain 이 자동
  - system_instruction → create_react_agent 의 prompt 인자로
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

NOTES_DIR = Path(__file__).parent.parent / "notes"


# === 도구 정의 (rag.py 의 함수 본문과 동일, @tool 데코레이터만 추가) ===
@tool
def search_notes(keyword: str) -> list[dict]:
    """notes 폴더에서 키워드와 매칭되는 파일들을 점수순으로 반환한다.

    회사 정책·회의록·온보딩 등 사내 문서에 대한 질문에 사용.
    """
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


# === LLM 연결 ===
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
)


# === 시스템 프롬프트 (rag.py 의 SYSTEM_INSTRUCTION 과 동일 역할) ===
SYSTEM_PROMPT = (
    "당신은 사내 노트를 검색해서 직원 질문에 답하는 도우미입니다. "
    "정책·규정·회의록에 관한 질문은 반드시 search_notes 로 먼저 검색한 뒤, "
    "검색 결과에 근거해서만 답하세요. "
    "검색 결과에 없는 내용은 추측하지 말고 '문서에 없습니다' 라고 답하세요."
)


# === ★ 이 한 줄이 rag.py 의 agent loop 전체에 해당 ===
agent = create_react_agent(llm, tools=[search_notes], prompt=SYSTEM_PROMPT)


if __name__ == "__main__":
    user_question = "신입사원인데 연차 언제부터 쓸 수 있어?"
    print(f"You: {user_question}\n")

    result = agent.invoke({"messages": [("user", user_question)]})

    # 전체 흐름 출력 — 어떤 도구가 호출되고 어떤 결과를 받았는지 보임
    for msg in result["messages"]:
        msg.pretty_print()
