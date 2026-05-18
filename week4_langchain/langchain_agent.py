"""
Week 4: LangChain — W3 rag.py 와 같은 일을 한 줄로.

학습 목표:
  - W3 rag.py 와 똑같은 결과 (사내 노트 검색 + 답변) 를 LangChain 으로
  - 우리가 직접 짠 100줄 골격이 = create_react_agent 한 줄 임을 눈으로 본다
  - "LangChain 도 결국 우리 골격 위의 편의 기능" 이 손에 잡힌다

실행:
  python langchain_agent.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

NOTES_DIR = Path(__file__).parent.parent / "notes"


# === 도구 정의 ===
# TODO (1): 아래 함수 위에 LangChain 의 @tool 데코레이터를 추가하세요.
#   생각해볼 거리: 이 데코레이터가 자동으로 만들어주는 것은?
#     - 함수 시그니처 → tool schema (W3 에서 직접 작성한 tool_declarations 가 불필요!)
#     - docstring → tool description
#   힌트: @tool

___
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


# === 시스템 프롬프트 (W3 의 SYSTEM_INSTRUCTION 과 동일 역할) ===
SYSTEM_PROMPT = (
    "당신은 사내 노트를 검색해서 직원 질문에 답하는 도우미입니다. "
    "정책·규정·회의록에 관한 질문은 반드시 search_notes 로 먼저 검색한 뒤, "
    "검색 결과에 근거해서만 답하세요. "
    "검색 결과에 없는 내용은 추측하지 말고 '문서에 없습니다' 라고 답하세요."
)


# TODO (2): create_react_agent 한 줄로 agent 만들기.
#   생각해볼 거리: 이 한 줄 안에 W3 rag.py 의 무엇이 들어있을까?
#     - while 루프? function_call 처리? function_response 형식? MAX_TURNS?
#   힌트: create_react_agent(llm, tools=[search_notes], prompt=SYSTEM_PROMPT)
agent = ___


if __name__ == "__main__":
    user_question = "신입사원인데 연차 언제부터 쓸 수 있어?"
    print(f"You: {user_question}\n")

    result = agent.invoke({"messages": [("user", user_question)]})

    # 전체 흐름 출력 — 어떤 도구가 호출되고 어떤 결과를 받았는지 보임
    for msg in result["messages"]:
        msg.pretty_print()
