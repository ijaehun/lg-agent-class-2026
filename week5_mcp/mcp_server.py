"""
Step 6: MCP 서버 — rag.py 의 search_docs 를 MCP 표준으로 노출.

학습 목표:
  - rag.py 의 search_docs 와 로직은 완전히 같다.
  - 바뀐 것은 단 두 줄:
      ① FastMCP 객체 생성
      ② @mcp.tool() 데코레이터
  - 이 두 줄이 "내 도구를 Claude Desktop / Cursor 등 어떤 MCP 클라이언트에도
    꽂을 수 있게 만드는" 표준 어댑터 (= USB-C).

실행:
  python mcp_server.py
  (stdio 로 클라이언트의 연결을 기다림 — 직접 실행하면 멈춰있는 것처럼 보임)

  실제 사용은 Claude Desktop 에 등록해서 사용. README.md 참고.
"""

from mcp.server.fastmcp import FastMCP


# === 사내 위키 (rag.py 와 동일) ===
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


# TODO (1): MCP 서버 인스턴스를 생성하세요.
#   힌트: mcp = FastMCP("company-wiki")
#   "company-wiki" 는 서버 이름 (클라이언트 쪽에 노출됨).
___


# TODO (2): 아래 search_docs 함수를 MCP 도구로 등록하는 데코레이터를 추가하세요.
#   힌트: 함수 정의 바로 위에 @mcp.tool()
#   이 데코레이터 한 줄이 "이 함수를 외부 MCP 클라이언트에 노출" 의 전부.
@___
def search_docs(query: str) -> list[dict]:
    """사내 위키에서 키워드로 관련 문서를 검색한다. 회사 정책·규정·복지 관련 질문에 사용."""
    keywords = query.lower().split()
    scored = []
    for doc in DOCS:
        text = (doc["title"] + " " + doc["content"]).lower()
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scored.append((score, doc))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [doc for _, doc in scored[:3]]


if __name__ == "__main__":
    # 기본 transport 는 stdio — 클라이언트가 이 프로세스를 띄우고 표준 입출력으로 통신
    mcp.run()
