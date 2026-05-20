---
marp: true
theme: default
paginate: true
size: 16:9
header: 'LG KAMP · AI 에이전트 강의 · W3'
footer: '2026'
style: |
  section {
    font-size: 28px;
    background: linear-gradient(180deg, #fafbfc 0%, #ffffff 100%);
    font-family: 'Pretendard', 'Noto Sans KR', -apple-system, system-ui, sans-serif;
    color: #202124;
  }
  section.lead {
    background: linear-gradient(135deg, #e8f0fe 0%, #ffffff 100%);
  }
  h1 {
    color: #1a73e8;
    border-bottom: 3px solid #1a73e8;
    padding-bottom: 8px;
    letter-spacing: -0.5px;
  }
  h2 {
    color: #333;
  }
  strong {
    color: #d93025;
  }
  table {
    font-size: 24px;
    border-collapse: collapse;
    margin: 12px auto;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    border-radius: 8px;
    overflow: hidden;
  }
  th {
    background: #1a73e8;
    color: white;
    padding: 12px 16px;
    font-weight: 600;
  }
  td {
    padding: 10px 16px;
    border-bottom: 1px solid #e8eaed;
    background: white;
  }
  tr:last-child td {
    border-bottom: none;
  }
  code {
    background: #f1f3f4;
    padding: 2px 6px;
    border-radius: 4px;
    color: #d93025;
    font-family: 'JetBrains Mono', 'D2Coding', 'Consolas', monospace;
  }
  pre {
    background: #f8f9fa;
    border-radius: 10px;
    padding: 14px 18px !important;
    border: 1px solid #e8eaed;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  }
  pre code {
    font-size: 19px;
    line-height: 1.45;
    color: #202124;
    background: transparent;
    font-family: 'JetBrains Mono', 'D2Coding', 'Consolas', monospace;
  }
  blockquote {
    border-left: 4px solid #1a73e8;
    background: #f1f7ff;
    padding: 12px 20px;
    margin: 18px 0;
    color: #444;
    border-radius: 0 6px 6px 0;
  }
  /* Roadmap boxes */
  .roadmap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin: 30px 0;
    flex-wrap: nowrap;
  }
  .step {
    padding: 16px 12px;
    border: 2px solid #dadce0;
    border-radius: 12px;
    min-width: 130px;
    text-align: center;
    background: white;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
  }
  .step .num {
    font-size: 22px;
    font-weight: bold;
    color: #1a73e8;
    display: block;
    margin-bottom: 4px;
  }
  .step .title {
    font-size: 18px;
    font-weight: 600;
    display: block;
    margin-bottom: 4px;
  }
  .step .sub {
    font-size: 14px;
    color: #666;
    display: block;
  }
  .step.current {
    background: #1a73e8;
    border-color: #1a73e8;
    transform: scale(1.08);
    box-shadow: 0 4px 12px rgba(26,115,232,0.4);
  }
  .step.current .num,
  .step.current .title,
  .step.current .sub {
    color: white;
  }
  .arrow {
    font-size: 26px;
    color: #999;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Week 3
## MCP — 도구의 표준 단자

마지막 회차 · **종강**

---

# 3주 로드맵 — 마지막

<div class="roadmap">
  <div class="step">
    <span class="num">W1</span>
    <span class="title">LLM + 에이전트</span>
    <span class="sub">RAG 맛</span>
  </div>
  <div class="arrow">→</div>
  <div class="step">
    <span class="num">W2</span>
    <span class="title">RAG 심화</span>
    <span class="sub">+ LangChain</span>
  </div>
  <div class="arrow">→</div>
  <div class="step current">
    <span class="num">W3</span>
    <span class="title">오늘</span>
    <span class="sub">MCP<br/>+ 종강</span>
  </div>
</div>

지금까지: 도구가 **우리 코드 안** 에 있었음.
오늘: 도구를 **외부에 표준으로** 노출. 다른 클라이언트도 사용 가능.

---

# 오늘 끝나면 답할 수 있어야

1. MCP 가 왜 필요한가? 도구를 코드에 박아둔 것의 문제는?
2. `rag.py` 의 `search_notes` ↔ `mcp_server.py` 의 `search_notes` — **다른 줄이 몇 줄?**
3. Claude Desktop 이 우리 서버를 어떻게 찾고 호출하나?
4. 본인 업무 도구를 MCP 서버로 만드는 길이 머리에 그려지는가?

★ 4번이 **종강의 진짜 목표** — 자기 업무로 가져갈 수 있는가.

---

<!-- _class: lead -->

# 왜 MCP?

지금까지 우리는:
- W1: 도구를 우리 Python 코드 안에 박았음
- W2: LangChain 으로 추상화했지만 여전히 **본인 코드 안**

문제:
- **다른 사람이 못 씀** (예: Claude Desktop, Cursor, ChatGPT)
- 매번 직접 agent loop 돌려야 함
- 도구 = 코드와 강결합

**MCP** = Model Context Protocol — **도구를 외부에 표준으로 노출.**

> **USB-C 비유**:
> 충전기마다 단자 다르면 불편 → USB-C 로 표준화.
> 도구마다 호출 방식 다르면 불편 → MCP 로 표준화.

---

# MCP 의 그림

```
[Claude Desktop / Cursor / Other Client]
            ↓ MCP 프로토콜 (stdio / HTTP)
[Our MCP Server: mcp_server.py]
            ↓
[search_notes(keyword)]
            ↓
[notes/ 폴더 검색 결과]
```

→ **클라이언트는 우리 코드를 몰라도 됨.** 표준 단자만 알면 됨.

지금까지: 우리가 LLM 호출 + 도구 실행 다 함
**MCP**: 도구만 노출하고 호출은 클라이언트가.

---

# 핵심 변화 — 두 줄

`rag.py` 의 `search_notes` 함수를 그대로 + **두 줄만 추가**:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("notes-agent")      # 1. 서버 인스턴스

@mcp.tool()                        # 2. 함수를 도구로 노출
def search_notes(keyword: str) -> list[dict]:
    """notes 에서 keyword 검색"""
    ...

if __name__ == "__main__":
    mcp.run()                      # 3. 서버 시작 (stdio 대기)
```

> **함수 본문은 W2 와 100% 동일.**
> 데코레이터 한 줄로 표준 도구화.

---

# `mcp_server.py` 분해

```python
from pathlib import Path
from mcp.server.fastmcp import FastMCP

NOTES_DIR = Path(__file__).parent.parent / "notes"

mcp = FastMCP("notes-agent")   # ★ 1. 서버 객체

@mcp.tool()                     # ★ 2. 데코레이터
def search_notes(keyword: str) -> list[dict]:
    """notes 에서 키워드 검색 (회사 정책·회의록·온보딩)."""
    keywords = keyword.lower().split()
    results = []
    for path in NOTES_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8").lower()
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            results.append({"score": score, "filename": path.name, ...})
    results.sort(key=lambda x: -x["score"])
    return results[:3]

if __name__ == "__main__":
    mcp.run()                    # ★ 3. 서버 실행
```

---

# `rag.py` ↔ `mcp_server.py` 비교

| | `rag.py` (W2) | `mcp_server.py` (W3) |
|---|---|---|
| `search_notes` 함수 본문 | 동일 | 동일 |
| `tool_declarations` (15줄) | 직접 작성 | **없음** (`@mcp.tool()` 가 자동) |
| LLM 호출 / agent loop | 우리가 작성 | **없음** (클라이언트가 함) |
| `system_instruction` | 우리가 작성 | **없음** (클라이언트가 정의) |
| 추가된 줄 | — | `FastMCP("...")` + `@mcp.tool()` + `mcp.run()` |

> **MCP 화는 두 줄.** 우리 도구를 외부 클라이언트가 쓸 수 있게.

---

# 실행 — stdio 대기

```bash
python mcp_server.py
```

⚠️ **출력 없이 멈춰 있는 것처럼 보임 — 정상.**
stdio 로 클라이언트의 연결을 기다리는 상태. `Ctrl+C` 로 종료.

> "서버" 라 응답할 일이 있을 때만 동작. 평소엔 대기.

---

# Claude Desktop 등록 — 설정 파일

설정 위치:
| OS | 경로 |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

> Claude Desktop 의 `Settings → Developer → Edit Config` 로도 열 수 있음.

---

# Claude Desktop 등록 — 설정 내용 (Windows)

```json
{
  "mcpServers": {
    "notes-agent": {
      "command": "C:\\Users\\이름\\...\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\이름\\...\\week3_mcp\\mcp_server.py"]
    }
  }
}
```

⚠️ **venv 안의 python 사용** (시스템 python 이면 mcp 패키지 못 찾음)
⚠️ Windows JSON 의 `\` → `\\` 두 개

**Claude Desktop 완전 재시작** → 도구 아이콘에 `notes-agent` 가 보이면 성공.

---

# 실제 사용 — Claude Desktop 에서

테스트 프롬프트:
```
신입사원인데 연차 언제부터 쓸 수 있어?
```

Claude Desktop 의 내부 흐름:
```
1. Claude (LLM) 가 "notes-agent" 서버의 search_notes 부름
2. 우리 mcp_server.py 응답: [{policy_leave.md, ...}, ...]
3. Claude 가 결과 기반으로 자연어 답
```

→ **우리 코드 없이도** Claude Desktop 이 검색 + 답.
**우리는 도구만 제공.**

---

# ★ 망가뜨려보기 — MCP 도 약속 위에서

| 망가뜨릴 곳 | 결과 |
|---|---|
| `@mcp.tool()` 데코레이터 제거 | Claude Desktop 이 도구 인식 못 함 |
| docstring 빈 문자열 | Claude 가 도구 용도 몰라 안 부름 |
| Claude Desktop 안 재시작 | 새 설정 반영 안 됨 (재시작 필수) |
| venv 가 아닌 시스템 python | `ModuleNotFoundError: mcp` |

> 다시 한 번 — **docstring 한 줄이 도구의 운명을 결정.**
> W1 의 `description`, W2 의 docstring, W3 의 docstring — 같은 본질.

---

<!-- _class: lead -->

# 본인 도구 MCP 화

W2 에서 만든 본인 도구 → `my_mcp_server.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-agent")

@mcp.tool()
def my_tool(query: str) -> ...:
    """도구 설명 — 명확하게"""
    ...

if __name__ == "__main__":
    mcp.run()
```

Claude Desktop 설정에 추가하면 **본인 업무용 에이전트 완성.**

---

# 3주 전체 요약 — 한 줄씩 더한 것

```
W1 Part 1: hello.py        client.models.generate_content(...)
W1 Part 2: agent_loop.py   + 도구 + while 루프  ← 에이전트
W1 끝:     agent_skill.py  + search_notes      ← RAG 맛
W2 Part 1: rag.py          + system_instruction ← grounding
W2 Part 2: langchain        100줄 → 한 줄
W3 (오늘): mcp_server.py    데코레이터 한 줄 = 표준 도구화
```

**한 줄로**: 이 모든 게 W1 의 `generate_content(...)` 한 줄 위에 한 줄씩 더한 것.

---

<!-- _class: lead -->

# 핵심 종강 메시지

> "여러분이 3주에 배운 게 곧 에이전트의 전부.
>
> LangChain · CrewAI 는 우리 골격 위의 편의 기능,
> MCP 는 그 도구를 표준화한 것.
>
> **실무 자동화 = 같은 골격 + 회사에 맞는 도구.**"

---

<!-- _class: lead -->

# 강의 후 다음 단계

- **본인 도구 1~2 개 더** — agent loop 의 도구 자리에 끼워넣기
- **MCP 공식 문서**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Anthropic / GitHub 의 MCP 서버 카탈로그** — 오픈소스 도구 다수
- **LangGraph 깊게** — W2 에서 본 패턴의 확장

6개월 뒤 본인이 만든 에이전트 자랑하러 와주시면 좋겠습니다.

---

<!-- _class: lead -->

# 감사합니다 🙏

> "오늘 이후 자기 업무에 적용할 때 막히면,
> **도구 함수만 새로 짜고 골격은 그대로 두세요.**
>
> 그게 정답이에요."
