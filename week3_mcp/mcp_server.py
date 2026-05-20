"""W3: MCP 서버 — rag.py 의 search_notes 를 MCP 표준으로 노출 (베이스라인).

핵심:
  - rag.py 의 search_notes 와 함수 본문은 완전히 동일
  - 바뀐 것은 단 두 줄:
      ① FastMCP 객체 생성
      ② @mcp.tool() 데코레이터
  - 이 두 줄이 "내 도구를 Claude Desktop / Cursor 등 어떤 MCP 클라이언트에도
    꽂을 수 있게 만드는" 표준 어댑터 (= USB-C)

실행:
  python mcp_server.py
  (stdio 로 클라이언트의 연결을 기다림 — 직접 실행하면 멈춰있는 것처럼 보임)

  실제 사용은 Claude Desktop 에 등록해서 사용. README.md 참고.
"""

from pathlib import Path
from mcp.server.fastmcp import FastMCP


NOTES_DIR = Path(__file__).parent.parent / "notes"


# === [1] MCP 서버 인스턴스 ===
# 서버 이름 ("notes-agent") 은 Claude Desktop 등 클라이언트에서 보임
mcp = FastMCP("notes-agent")


# === [2] @mcp.tool() — 함수를 MCP 도구로 자동 등록 ===
# 함수 시그니처 + docstring → MCP 표준 스키마 자동 생성
# (rag.py 의 tool_declarations 가 더 이상 필요 없음)
@mcp.tool()
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


if __name__ == "__main__":
    # 기본 transport 는 stdio — 클라이언트가 이 프로세스를 띄우고 표준 입출력으로 통신
    mcp.run()
