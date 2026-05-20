# Week 3 — MCP 표준 + 종강

마지막 회차. **MCP 도입** + **Claude Desktop 등록** + **본인 도구 MCP 화** + **3주 요약 + 종강**.

## 이번 주에 배우는 것

- **MCP** = Model Context Protocol — 도구의 USB-C
- `FastMCP` 로 우리 도구를 외부 클라이언트 (Claude Desktop, Cursor 등) 에 노출
- `@mcp.tool()` 데코레이터 한 줄로 함수를 표준 도구화
- Claude Desktop 에 등록해서 **진짜 클라이언트가 우리 서버를 호출하는 것** 을 눈으로 본다
- **본인 업무 도구** 를 MCP 서버로 만들기 — 강의의 종착점

## 회차 끝나면 답할 수 있어야 하는 질문

1. MCP 가 왜 필요한가? 지금까지 도구를 코드에 박아둔 것의 문제는?
2. W2 의 `rag.py` 의 `search_notes` 와 `mcp_server.py` 의 `search_notes` 의 차이를 코드로 짚을 수 있는가?
3. Claude Desktop 이 우리 서버를 어떻게 찾고 호출하나?
4. 본인 업무 도구를 MCP 서버로 만드는 길이 머리에 그려지는가?

→ **4번이 종강의 진짜 목표** — 자기 업무로 가져갈 수 있는가.

---

## 3주 시나리오 — 마지막

| 주차 | 무엇 |
|---|---|
| W1 | LLM + 에이전트 + RAG 맛 (`agent_skill.py` 까지) |
| W2 | RAG 심화 + LangChain (`create_react_agent` 한 줄) |
| **W3 (오늘)** | **MCP** — 도구를 표준 단자로 + 종강 |

→ **3주 전체에서 골격은 그대로. 도구만 추가 / 표준화.**

---

## 무엇을 만들 건가

| 파일 | 역할 |
|---|---|
| `mcp_server.py` | W2 `rag.py` 의 `search_notes` 를 MCP 표준으로 노출 |
| `my_mcp_server.py` (직접) | **본인 업무 도구** 를 MCP 서버로 |

사용 흐름:
```
사용자 (Claude Desktop) → 자연어 질문
↓
Claude (LLM) → notes-agent 서버 호출
↓
우리 mcp_server.py → search_notes("연차 신입") → 결과 반환
↓
Claude → 결과 기반으로 자연어 답변
```

## 어떻게 접근하나 — 바이브 코딩 사고법

### 단계별 사고

**1. 내가 뭘 만들 건가?**
도구를 **외부 클라이언트에 표준 단자로 노출** 해서, 우리 코드 없이도 Claude Desktop 같은 도구가 그 도구를 부를 수 있게.

**2. 어떤 구조?**
`rag.py` 의 `search_notes` 함수 + 두 줄 추가:
```python
mcp = FastMCP("notes-agent")    # 서버 인스턴스

@mcp.tool()                       # 함수를 도구로 노출하는 데코레이터
def search_notes(query): ...
```
**다른 코드는 거의 없음.** 도구 함수 자체는 `rag.py` 와 동일.

**3. 어떻게 실행되나?**
- 우리 `mcp_server.py` 는 stdio 로 클라이언트의 연결을 기다림
- Claude Desktop 의 설정 파일에 우리 서버를 등록
- Claude Desktop 이 우리 서버 프로세스를 띄우고, 도구 호출 시 stdio 로 통신

**4. 본인 도구를 MCP 화 하는 법?**
W2 에서 만든 본인 도구 함수 위에 `@mcp.tool()` 한 줄 + `mcp = FastMCP("이름")` + `mcp.run()`. 끝.

→ "MCP 화 = 함수 위 데코레이터 한 줄" 이라는 단순함이 본질.

---

## 직접 해야 하는 것

### (1) 손으로 짜보기 — `mcp_server.py`

```bash
cd week3_mcp
python mcp_server.py
```

⚠️ 실행하면 **출력 없이 멈춰 있는 것처럼 보임** — 정상이에요. stdio 로 클라이언트의 연결을 기다리는 상태. `Ctrl+C` 로 종료.

TODO 두 개:
- `mcp = FastMCP("notes-agent")` 인스턴스 생성
- `@mcp.tool()` 데코레이터 추가

**생각해볼 거리**:
- 데코레이터 한 줄로 무엇이 자동화되나? (도구 스키마 자동 생성 — W2 `rag.py` 에서 직접 작성한 `tool_declarations` 가 필요 없어요)
- 함수 시그니처 (`query: str -> list[dict]`) 와 docstring 이 MCP 표준 스키마로 변환됩니다.

### (2) `rag.py` ↔ `mcp_server.py` 비교

두 파일을 나란히 열어 차이를 봐보세요:
- `search_notes` 함수 본문: **완전 동일** (notes/ 폴더 검색 + 점수 계산)
- 차이: `FastMCP` 객체 + `@mcp.tool()` 데코레이터 두 줄
- 추가로 W2 의 `tool_declarations` (15줄짜리 스키마) 가 필요 없어짐 — 데코레이터가 자동 생성

→ "MCP 화는 두 줄로 끝" 이라는 단순함 체감.

### (3) 망가뜨려보기

| 망가뜨릴 곳 | 결과 |
|---|---|
| `@mcp.tool()` 데코레이터 제거 | Claude Desktop 이 도구 인식 못 함 |
| docstring 빈 문자열 | Claude 가 도구 용도 몰라 안 부름 |
| Claude Desktop 안 재시작 | 새 설정 반영 안 됨 (재시작 필수) |
| venv 가 아닌 시스템 python | `ModuleNotFoundError: mcp` |

→ docstring = MCP 에서의 description. W1 의 `description`, W2 의 docstring 과 **같은 본질**.

### (4) Claude Desktop 등록

**(a) Claude Desktop 설치** ([claude.ai/download](https://claude.ai/download))

**(b) 설정 파일 위치**:
| OS | 경로 |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

> Claude Desktop 의 `Settings → Developer → Edit Config` 로도 열 수 있어요.

**(c) 설정 입력** — 본인 환경 절대 경로로:

Windows:
```json
{
  "mcpServers": {
    "notes-agent": {
      "command": "C:\\Users\\이름\\Dropbox\\github\\lg-agent-class-2026\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\이름\\Dropbox\\github\\lg-agent-class-2026\\week3_mcp\\mcp_server.py"]
    }
  }
}
```

macOS:
```json
{
  "mcpServers": {
    "notes-agent": {
      "command": "/Users/이름/lg-agent-class-2026/.venv/bin/python3",
      "args": ["/Users/이름/lg-agent-class-2026/week3_mcp/mcp_server.py"]
    }
  }
}
```

⚠️ **반드시 venv 안의 python** (시스템 python 이면 mcp 패키지 못 찾음)
⚠️ Windows JSON 의 `\` → `\\` 두 개

**(d) Claude Desktop 완전 재시작** → 도구 아이콘에 `notes-agent` 가 보이면 성공.

**(e) 테스트 프롬프트**:
```
신입사원인데 연차 언제부터 쓸 수 있어?
```
→ Claude 가 `search_notes` 호출 → 우리 mcp_server 응답 → Claude 의 자연어 답변.

### (5) ★ 본인 도구 MCP 화 — 강의의 종착점

W2 에서 만든 본인 도구 함수를 `my_mcp_server.py` 로:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-agent")

@mcp.tool()
def my_tool(...) -> ...:
    """도구 설명 — 명확하게"""
    ...

if __name__ == "__main__":
    mcp.run()
```

Claude Desktop 설정에 추가하면 **본인 업무용 에이전트 완성**.

**짝꿍과 시연**:
- 짝꿍의 도구를 본인 Claude Desktop 에 임시 등록 → 사용해보기
- 피드백: "docstring 명확한가? Claude 가 적절히 부르는가? 결과 형식이 LLM 이 답하기 좋은가?"

---

## 3주 전체 요약

```
W1 Part 1: hello.py        client.models.generate_content(...)
W1 Part 2: agent_loop.py   + 도구 + while 루프  ← 에이전트의 정체
W1 끝:     agent_skill.py  + search_notes      ← RAG 맛
W2 Part 1: rag.py          + system_instruction ← grounding
W2 Part 2: langchain        100줄 → 한 줄 (create_react_agent)
W3 (오늘): mcp_server.py    데코레이터 한 줄로 표준 도구화
```

**한 줄로**: 이 모든 게 W1 의 `generate_content(...)` 한 줄 위에 한 줄씩 더한 것.

## 핵심 종강 메시지

> "여러분이 3주에 배운 게 곧 에이전트의 전부.
> LangChain · CrewAI 는 우리 골격 위의 편의 기능, MCP 는 그 도구를 표준화한 것.
> 실무 자동화 = **같은 골격 + 회사에 맞는 도구**.
>
> 오늘 이후 자기 업무에 적용할 때 막히면, 도구 함수만 새로 짜고 골격은 그대로 두세요.
> 그게 정답이에요."

## 강의 후 다음 단계

- **본인 도구 1~2 개 더 만들기** — agent loop 의 도구 자리에 끼워넣기
- **MCP 공식 문서**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Anthropic / GitHub 의 MCP 서버 카탈로그** — 오픈소스 도구 다수 (그대로 가져다 쓸 수 있어요)
- **LangGraph 깊게** — W2 에서 본 패턴의 확장

6개월 뒤 본인이 만든 에이전트 자랑하러 와주시면 좋겠습니다.
