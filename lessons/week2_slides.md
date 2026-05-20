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

# Week 2
## RAG 심화 + LangChain

W1 골격 → 한 단계 더 + 한 줄로

---

# 3주 로드맵

<div class="roadmap">
  <div class="step">
    <span class="num">W1</span>
    <span class="title">LLM + 에이전트</span>
    <span class="sub">+ RAG 맛</span>
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

지난주 우리는 `agent_skill.py` 로 **RAG 의 본질** 을 봤죠.
오늘은 그 위에 두 가지: **grounding + LangChain 한 줄.**

---

# 오늘 끝나면 답할 수 있어야

1. W1 의 `agent_skill.py` 와 `rag.py` 의 차이를 코드로 짚을 수 있나?
2. `system_instruction` 이 없으면 LLM 이 어떻게 답할까?
3. `create_react_agent` **한 줄 안에서 일어나는 일** 을 본인 입으로 설명할 수 있는가?
4. LangChain 을 쓰면 좋은 상황 / 직접 짜면 좋은 상황은?
5. Copilot 한테 LangChain agent 짜달라고 했을 때, 답이 옳은지 평가할 수 있는가?

★ **3번이 가장 중요** — "한 줄 안의 정체" 를 알아야 LangChain 을 진짜 쓰는 것.

---

<!-- _class: lead -->

# 오늘 진행 방식

지난주와 **같은 4단계**:

| | 단계 | 무엇을 |
|---|---|---|
| **1** | **구조** | 그림으로 — system_instruction / LangChain 한 줄의 의미 |
| **2** | **손코딩** | TODO 채우기 + **망가뜨려보기** |
| **3** | **Copilot** | 같은 LangChain agent 시켜보기 |
| **4** | **해석** | 받은 코드 평가 — 우리 골격 ↔ LangChain 비교 |

> 오늘은 손코딩이 짧음 — 개념이 W1 의 확장이라.
> 대신 **비교 + 평가** 에 시간 많이.

---

<!-- _class: lead -->

# 📘 Part 1 — RAG 심화

`rag.py` + `notes_agent.py`

W1 의 `agent_skill.py` 위에 **`system_instruction` 한 줄**.
그게 grounding (할루시네이션 방지).

---

# W1 의 한계 — 할루시네이션은 막을 수 없음

W1 의 `agent_skill.py`:
- 검색 도구 (`search_notes`) 있음
- 근데 LLM 이 **검색 안 하고 그냥 답할 수도 있음**
- 검색 결과 없으면 **추측해서 답할 수도** = 할루시네이션

```python
# 빈 결과 받고도 그럴듯하게 답함
[도구 결과] []
Model: 일반적으로 신입사원은 3개월 후부터 연차를...   ← 추측!
```

> 이걸 어떻게 강제할까? → **`system_instruction` 한 줄.**

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

> **이 한 줄이 RAG 의 두 번째 본질** — 검색 결과에 **근거** 하라는 강제.

---

# `rag.py` 분해 — 골격은 W1 과 동일

```python
# 도구 — search_notes (W1 과 동일하지만 점수 계산 추가)
def search_notes(keyword: str) -> list[dict]:
    """notes/ 폴더에서 keyword 매칭 + 점수순 정렬"""
    ...

# ★ 새로 추가: system_instruction
SYSTEM_INSTRUCTION = "검색 결과에 근거해 답하라..."

config = types.GenerateContentConfig(
    tools=[types.Tool(function_declarations=[search_notes_declaration])],
    system_instruction=SYSTEM_INSTRUCTION,
)

# Agent loop — W1 과 100% 동일 (30줄)
for turn in range(MAX_TURNS):
    ...
```

> **W1 agent_skill.py 와 다른 줄**: `system_instruction` 한 줄.
> agent loop 본문은 **안 변함.**

---

# ★ 망가뜨려보기 — system_instruction 의 힘

| 망가뜨릴 곳 | 결과 |
|---|---|
| `SYSTEM_INSTRUCTION` 을 `""` 로 | LLM 이 검색 안 하고 추측해서 답할 수도 |
| `search_notes` description 을 `""` 로 | LLM 이 도구를 안 부름 |
| `search_notes` 가 빈 리스트 반환 | LLM 이 "문서에 없습니다" 답해야 옳음 — 실제 그런지 확인 |

→ 같은 질문에 system_instruction **있을 때 vs 없을 때** 답이 어떻게 달라지나?

> system_instruction = **약속 + 강제**.
> LLM 한테 "이렇게 행동해" 라고 명시.

---

# 실전 — `notes_agent.py`

도구 3개 통합 (`list_notes`, `read_note`, `search_notes`)

```python
TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
    "search_notes": search_notes,
}

# system_instruction + tool_declarations 3개
# 환경변수로 본인 폴더 지정 가능
NOTES_DIR = Path(os.environ.get("NOTES_DIR", str(DEFAULT_NOTES_DIR)))
```

본인 폴더로 실행:
```powershell
$env:NOTES_DIR="C:\본인\문서폴더"; python notes_agent.py
```

→ "내 진짜 노트" 로 실험. **LLM 이 알아서 적절한 도구 골라 부름.**

---

<!-- _class: lead -->

# 🔗 Part 2 — LangChain 한 줄로

`langchain_agent.py`

Part 1 에서 짠 100줄 = `create_react_agent` **한 줄**.

---

# LangChain 이 자동으로 해주는 것

| 우리 (Part 1) | LangChain |
|---|---|
| `tool_declarations` 직접 작성 (15줄) | `@tool` 데코레이터 (1줄) |
| `TOOL_FUNCTIONS` 딕셔너리 | 자동 |
| `for turn in range(MAX_TURNS)` 루프 | 자동 |
| `function_calls` 추출 | 자동 |
| 종료 조건 `if not function_calls: break` | 자동 |
| `function_response` 형식 | 자동 |
| `history.append(...)` | 자동 |
| `system_instruction` | `prompt=` 인자로 |

→ **Part 1 에 한 줄씩 짠 모든 것이 자동.**

---

# `langchain_agent.py` 분해 — 한 줄

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool

# 1. ★ 도구 — @tool 데코레이터만 (스키마 자동 생성)
@tool
def search_notes(keyword: str) -> list[dict]:
    """notes/ 에서 keyword 검색"""
    ...

# 2. LLM
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

# 3. ★ 핵심 한 줄
agent = create_react_agent(llm, tools=[search_notes], prompt=SYSTEM_PROMPT)

# 4. 실행
result = agent.invoke({"messages": [("user", "신입 연차 정책?")]})
```

> **3번 한 줄** 안에 Part 1 의 30줄 agent loop 가 들어있음.

---

# 줄 단위 비교 — Part 1 vs Part 2

| | `rag.py` | `langchain_agent.py` |
|---|---|---|
| 도구 스키마 | `tool_declarations` (15줄) | `@tool` (1줄) |
| TOOL_FUNCTIONS | dict 직접 | 없음 |
| while 루프 | `for turn in range(...)` | 없음 |
| function_call 추출 | 직접 | 없음 |
| 종료 조건 | `if not function_calls: break` | 없음 |
| function_response | 직접 dict 작성 | 없음 |
| system 강제 | `system_instruction=` | `prompt=` |

**100줄 → 30줄. 핵심 한 줄 = `create_react_agent`.**

---

# ★ 망가뜨려보기 — LangChain 도 약속 위에서 동작

| 망가뜨릴 곳 | 결과 |
|---|---|
| `@tool` 데코레이터 제거 | `create_react_agent` 가 도구 인식 못 함 |
| docstring 빈 문자열 | LLM 이 도구가 뭐 하는지 몰라 안 부름 |
| `prompt=` 빼기 | LLM 이 검색 안 하고 추측해서 답할 수도 |

→ "LangChain 도 결국 약속된 형식 위에서 동작" 이라는 본질 체감.

> docstring = LangChain 에서의 description.
> `@tool` 데코레이터 = `tool_declarations` 자동 생성기.

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

> **Part 1 에 print 로 찍던 것 = LangChain 의 messages.**
> 본질은 같음 — turn 별 메시지 리스트.

---

# 그럼 LangChain 만 쓰면 되지 왜 직접 짰나?

- **블랙박스 안에서 뭐 일어나는지** 알고 있어야 디버깅 가능
- 커스터마이징 때 결정적 차이 (예: 도구 결과 후처리, 토큰 절약)
- **Copilot 한테 시켜도 답이 옳은지 평가** 가능

> "LangChain 을 쓰는 사람" vs "**LangChain 의 정체를 아는 사람**".
> 두 번째가 5주의 목적.

---

<!-- _class: lead -->

# Copilot 한테 LangChain agent 시키기

빈 `my_lc_agent.py` → 프롬프트:

```
LangChain (LangGraph) 의 create_react_agent 로 사내 노트
검색 agent 를 짜줘.
- LLM: ChatGoogleGenerativeAI, gemini-3.5-flash
- 도구: search_notes — @tool 데코레이터
- system prompt: "검색해서 답하라, 없으면 '문서에 없습니다'"
- 사용자 질문: "신입사원 연차 정책 알려줘"
```

**짝꿍과 비교 — 체크리스트는 이제 너희가 만든다**:
- 어떤 줄이 핵심? 어떤 줄이 부속?
- Copilot 답에 빠진 게 있나? 추가된 게 있나?
- 우리 솔루션과 비교해서 어느 게 더 옳은가?

---

# 오늘 핵심 두 줄

1. **`system_instruction` 한 줄 = 할루시네이션 강제 차단**
   (W1 에서 본 RAG 의 본질을 강하게)

2. **`create_react_agent` 한 줄 = 우리 골격 100줄의 자동화**
   (LangChain 의 가치 = 추상화. 우리 가치 = 그 정체를 안다는 것)

---

<!-- _class: lead -->

# 다음 주 예고 — W3 MCP

지금까지: 도구를 **우리 코드 안** 에 박았음.

**W3 = 도구를 외부에 표준으로 노출.**

`@mcp.tool()` 데코레이터 **한 줄** + Claude Desktop 등록 → 우리 노트 검색 도구를 **Claude Desktop 에서 직접 사용.**

> "MCP = 도구의 USB-C."
> 우리가 만든 검색 도구를 **다른 클라이언트 (Claude Desktop, Cursor) 도 쓸 수 있게.**
