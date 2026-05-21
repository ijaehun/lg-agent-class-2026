---
marp: true
theme: default
paginate: true
size: 16:9
header: 'LG KAMP · AI 에이전트 강의 · W2'
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
  .week-flow {
    display: flex;
    flex-direction: column;
    gap: 18px;
    margin: 20px 0;
  }
  .part-row {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .part-title {
    font-size: 20px;
    font-weight: bold;
    color: #1a73e8;
    padding: 6px 14px;
    background: #e8f0fe;
    border-radius: 6px;
    align-self: flex-start;
  }
  .part-sub {
    font-size: 15px;
    color: #555;
    padding-left: 14px;
    margin-top: -4px;
  }
  .files-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: nowrap;
    padding-left: 8px;
  }
  .file-box {
    padding: 10px 12px;
    border: 2px solid #1a73e8;
    border-radius: 10px;
    background: white;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06);
    text-align: center;
    min-width: 120px;
  }
  .file-name {
    display: block;
    font-family: 'JetBrains Mono', 'D2Coding', 'Consolas', monospace;
    font-size: 16px;
    font-weight: bold;
    color: #d93025;
  }
  .file-desc {
    display: block;
    font-size: 13px;
    color: #555;
    margin-top: 4px;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Week 2
## 나만의 에이전트 만들기

---

# 3주 로드맵

<div class="roadmap">
  <div class="step">
    <span class="num">W1</span>
    <span class="title">LLM + 에이전트</span>
    <span class="sub">기본</span>
  </div>
  <div class="arrow">→</div>
  <div class="step current">
    <span class="num">W2</span>
    <span class="title">오늘</span>
    <span class="sub">RAG 심화<br/>+ LangChain</span>
  </div>
  <div class="arrow">→</div>
  <div class="step">
    <span class="num">W3</span>
    <span class="title">MCP</span>
    <span class="sub">도구의<br/>표준 단자</span>
  </div>
</div>

W1 의 에이전트 위에 **grounding (RAG) + 추상화 (LangChain)** 추가

---

# 오늘의 학습 흐름

<div class="week-flow">
  <div class="part-row">
    <div class="part-title">📘 Part 1 — RAG 심화</div>
    <div class="part-sub">검색 결과에 근거한 답변 (할루시네이션 방지)</div>
    <div class="files-row">
      <div class="file-box">
        <span class="file-name">rag.py</span>
        <span class="file-desc">검색 + grounding</span>
      </div>
      <div class="arrow">→</div>
      <div class="file-box">
        <span class="file-name">notes_agent.py</span>
        <span class="file-desc">실전 (도구 3개)</span>
      </div>
    </div>
  </div>

  <div class="part-row">
    <div class="part-title">🔗 Part 2 — LangChain</div>
    <div class="part-sub">우리 골격을 한 줄로 추상화</div>
    <div class="files-row">
      <div class="file-box">
        <span class="file-name">langchain_agent.py</span>
        <span class="file-desc">create_react_agent</span>
      </div>
    </div>
  </div>
</div>

---

# 오늘의 학습 목표

1. W1 에이전트의 한계 — 할루시네이션이 왜 생기는가
2. `system_instruction` 한 줄로 어떻게 막는가 (RAG 의 본질)
3. LangChain `create_react_agent` 한 줄 안에서 일어나는 일
4. 우리 골격 ↔ LangChain — 같은 일을 어떻게 추상화하는가

★ 핵심 — **에이전트 골격은 같음. 추상화 / 강제만 추가.**

---

<!-- _class: lead -->

# 📘 Part 1 — RAG 심화

`rag.py` + `notes_agent.py`

검색 + `system_instruction` 으로 grounding 강제

---

# W1 에이전트의 한계 — 할루시네이션

W1 의 `agent_skill.py`:

- 검색 도구 (`search_notes`) 있음
- 근데 LLM 이 **검색 안 하고 그냥 답할 수도 있음**
- 검색 결과 없으면 **추측해서 답할 수도** = 할루시네이션

```python
# 빈 결과 받고도 그럴듯하게 답함
[도구 결과] []
Model: 일반적으로 신입사원은 3개월 후부터 연차를...   ← 추측!
```

→ **`system_instruction` 한 줄로 강제** 필요

---

# `system_instruction` — LLM 행동 강제

```python
SYSTEM_INSTRUCTION = """
당신은 사내 노트 검색 도우미입니다.

규칙:
1. 답하기 전에 반드시 search_notes 로 먼저 검색합니다.
2. 검색 결과에 없는 내용은 추측하지 마세요.
3. 결과가 없으면 "문서에 없습니다" 라고 정직하게 답합니다.
"""

config = types.GenerateContentConfig(
    tools=[...],
    system_instruction=SYSTEM_INSTRUCTION,    # ← 한 줄 추가
)
```

> **이 한 줄이 RAG 의 두 번째 본질** — 검색 결과에 **근거** 하라는 강제

---

# `rag.py` — 검색 + grounding

```python
def search_notes(keyword: str) -> list[dict]:
    """notes/ 에서 keyword 매칭 + 점수순 상위 3개 반환."""
    ...

SYSTEM_INSTRUCTION = "검색 결과에 근거해 답하라..."

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[search_notes_declaration])],
    system_instruction=SYSTEM_INSTRUCTION,    # ← 핵심
)

# Agent loop — W1 agent_loop 와 100% 동일 (30줄)
for turn in range(MAX_TURNS):
    ...
```

> **W1 `agent_skill.py` 와 다른 줄** = `system_instruction` 한 줄.
> agent loop 본문은 **안 변함.**

---

# Copilot 으로 직접 짜보기 — RAG

베이스라인 (`rag.py`) 본 후 → Copilot 으로 같은 RAG 짜보기

**Copilot 프롬프트 예시**

```
Gemini API 로 RAG 에이전트 짜줘.
- search_notes(keyword) 도구 — notes/ 폴더에서 키워드 매칭
- system_instruction 으로 "검색 결과에만 근거해 답하라" 강제
- agent loop (while + function_call 처리)
- 모델: gemini-2.5-flash
```

**비교** — Copilot 답이 베이스라인과 같은가?


---

# `notes_agent.py` — 실전 (도구 3개 통합)

W1 의 `list_notes` + `read_note` + `search_notes` 통합

```python
TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
    "search_notes": search_notes,
}

# 본인 폴더로 NOTES_DIR 변경 가능
NOTES_DIR = Path(os.environ.get("NOTES_DIR", str(DEFAULT_NOTES_DIR)))
```

질문 예시 (LLM 이 알아서 적절한 도구 선택):
- "출장비 정산 어떻게?" → `search_notes`
- "policy_remote.md 보여줘" → `read_note`
- "내 노트에 뭐 있어?" → `list_notes`

---

# Part 1 확장 실습 — 본인 폴더로

`NOTES_DIR` 환경변수로 본인 폴더 지정 → 본인 노트로 RAG 실험

```powershell
# Windows
$env:NOTES_DIR="C:\본인\문서폴더"; python notes_agent.py

# macOS
NOTES_DIR=/Users/본인/문서폴더 python3 notes_agent.py
```

**확장 아이디어**
- 본인 메모 / 회의록 폴더로 변경
- `system_instruction` 톤 바꾸기 (격식체 / 친근체)
- 검색 점수 알고리즘 개선 (단순 매칭 → 가중치)


---

# Part 1 정리

RAG 심화 완료

- `rag.py` — 검색 + `system_instruction` 으로 grounding
- `notes_agent.py` — 도구 3개 통합 실전
- 확장 실습 — 본인 폴더로 RAG 적용

> Part 2 에서 — 같은 일을 **LangChain 한 줄로**

---

<!-- _class: lead -->

# 🔗 Part 2 — LangChain

`langchain_agent.py`

Part 1 의 100줄 = `create_react_agent` **한 줄**

---

# LangChain 이 자동으로 해주는 것

| Part 1 (직접) | LangChain |
|---|---|
| `tool_declarations` 직접 작성 (15줄) | `@tool` 데코레이터 (1줄) |
| `TOOL_FUNCTIONS` dict | 자동 |
| `for turn in range(MAX_TURNS)` | 자동 |
| `function_call` 추출 | 자동 |
| 종료 조건 / `function_response` 형식 | 자동 |
| `system_instruction` | `prompt=` 인자로 |

→ Part 1 에 한 줄씩 짠 모든 것이 **자동화**

---

# `langchain_agent.py` — 핵심 한 줄

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# [1] 도구 — @tool 데코레이터만 (스키마 자동 생성)
@tool
def search_notes(keyword: str) -> list[dict]:
    """notes/ 에서 keyword 검색"""
    ...

# [2] LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# [3] ★ 핵심 한 줄
agent = create_react_agent(llm, tools=[search_notes], prompt=SYSTEM_PROMPT)

# [4] 실행
result = agent.invoke({"messages": [("user", "신입 연차 정책?")]})
```

> **3번 한 줄** 안에 Part 1 의 30줄 agent loop 가 들어있음

---

# Copilot 으로 직접 짜보기 — LangChain

베이스라인 (`langchain_agent.py`) 본 후 → Copilot 으로 같은 코드 짜보기

**Copilot 프롬프트 예시**

```
LangChain (LangGraph) 의 create_react_agent 로 사내 노트 검색 agent 짜줘.
- LLM: langchain_google_genai.ChatGoogleGenerativeAI, gemini-2.5-flash
- 도구: search_notes(keyword) — @tool 데코레이터
- system prompt: "검색해서 답하라, 없으면 '문서에 없습니다'"
- agent.invoke 로 실행 + result["messages"] 출력
```

**비교** — Copilot 답이 베이스라인과 같은가?


---

# 줄 단위 비교 — Part 1 vs Part 2

| | `rag.py` | `langchain_agent.py` |
|---|---|---|
| 도구 스키마 | `tool_declarations` (15줄) | `@tool` (1줄) |
| TOOL_FUNCTIONS | dict 직접 | 없음 |
| while 루프 | `for turn in range(...)` | 없음 |
| 종료 조건 | `if not function_calls: break` | 없음 |
| function_response | 직접 dict 작성 | 없음 |
| system 강제 | `system_instruction=` | `prompt=` |

**100줄 → 30줄**. 핵심 한 줄 = `create_react_agent`

---

# 디버깅 — `result["messages"]`

```python
result = agent.invoke({"messages": [("user", "신입 연차?")]})

for msg in result["messages"]:
    print(msg)
```

출력:
```
HumanMessage(content='신입 연차?')
AIMessage(tool_calls=[{'name': 'search_notes', 'args': {'keyword': '연차'}}])
ToolMessage(content='[{"file":"policy_leave.md","preview":"..."}]')
AIMessage(content='신입사원은 입사 후 6개월 동안...')
```

> Part 1 에 print 로 찍던 것 = LangChain 의 messages

---

# 그럼 LangChain 만 쓰면 되지 왜 직접 짰나?

- **블랙박스 안에서 뭐 일어나는지** 알고 있어야 디버깅 가능
- 커스터마이징 때 결정적 차이 (예: 도구 결과 후처리, 토큰 절약)
- **Copilot 한테 시켜도 답이 옳은지 평가** 가능

> "LangChain 을 쓰는 사람" vs "**LangChain 의 정체를 아는 사람**"

---

# Part 2 확장 실습 — 본인 도구를 LangChain 으로

W1 의 `agent_skill.py` 또는 본인 만든 도구를 LangChain 으로 변환

**과제**
- `@tool` 데코레이터로 본인 도구 감싸기
- `create_react_agent(llm, tools=[본인 도구], prompt=...)` 등록
- `result["messages"]` 출력으로 흐름 확인

**확장 아이디어**
- 여러 도구 동시 등록 (list + read + search + 본인 도구)
- `prompt` 변경해서 LLM 행동 바꿔보기


---

# Part 2 정리

LangChain 추상화 완료

- `langchain_agent.py` — `create_react_agent` 한 줄
- 줄 단위 비교 — 우리 100줄이 어떻게 한 줄에 들어갔는지
- 확장 실습 — 본인 도구를 LangChain 으로

> W3 에서 — 도구를 **외부에 표준으로** 노출 (MCP)

---

# 오늘 핵심 두 줄

1. **`system_instruction` 한 줄** = 할루시네이션 차단 (RAG 의 본질)
2. **`create_react_agent` 한 줄** = 우리 100줄의 자동화 (LangChain 의 본질)

---

<!-- _class: lead -->

# 다음 주 예고 — W3 MCP

지금까지: 도구가 **우리 코드 안** 에 있었음

**W3** = 도구를 **외부에 표준으로** 노출

`@mcp.tool()` 데코레이터 한 줄 + Claude Desktop 등록
→ 우리 검색 도구를 **Claude Desktop 에서 직접 사용**

> "MCP = 도구의 USB-C"
