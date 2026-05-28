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
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Week 2
## RAG + LangChain / LangGraph

---

# 지금까지의 흐름

<div class="roadmap">
  <div class="step">
    <span class="num">W1</span>
    <span class="title">LLM + 에이전트</span>
    <span class="sub">완료</span>
  </div>
  <div class="arrow">→</div>
  <div class="step current">
    <span class="num">W2</span>
    <span class="title">오늘</span>
    <span class="sub">RAG + LangChain<br/>/ LangGraph</span>
  </div>
</div>

오늘 = RAG + LangChain / LangGraph.

---

# 오늘 흐름

| 시간 | 파트 | 내용 |
|---|---|---|
| 5분 | **셋업** | venv + Jupyter 실행 + 모델 점검 |
| ~1h 50분 | **Part 1 — RAG** | keyword + vector 두 retriever + grounding |
| ~40분 | **Part 2 — LangChain / LangGraph** | W1 Agent + W2 RAG 한 줄 wrap |

---

<!-- _class: lead -->

# 📘 Part 1 — RAG

Retrieval + Augmented Generation

`week2.ipynb` — Part 1

---

# LLM 의 할루시네이션 문제

**할루시네이션 (hallucination)**
— LLM 이 모르는 내용을 그럴듯하게 지어내는 현상

**왜 발생하나**
- LLM = 인터넷 일반 데이터로 학습 → **우리 회사 내부 문서는 본 적 없음**
- 모르는 걸 물어봐도 "모릅니다" 가 아니라 추측 / 일반론으로 답함
- 모델이 거짓말하는 게 아니라, **모르는 걸 채워서 답하는 본성**

**예시**
```
질문: "신입사원은 연차 며칠 받아?"
LLM (그냥): "일반적으로 신입사원은 1년 후부터..."  ← 추측 / 일반론
```

→ 우리 `policy_leave.md` 의 실제 정책과 다를 수 있음.

---

# 해결 방법들

LLM 할루시네이션을 줄이는 대표적 접근:

1. **Fine-tuning** — 우리 데이터로 모델 재학습
   - 효과 크지만 **비싸고 느림.** 데이터 바뀌면 재학습
2. **system_instruction** — 답 형식 / 추측 금지 강제
   - 보통 RAG 와 함께 씀
3. **RAG** (Retrieval-Augmented Generation) — 답하기 전 관련 문서 찾아서 LLM 에게 같이 줌
   - **가볍고 빠름.** ← **오늘 다룰 방법**

---

# RAG = Retrieval-Augmented Generation

> "LLM 한테 그냥 묻지 말고,
> **답에 필요한 문서를 프롬프트에 같이 넣어서** 답하게 하자."

- **R**etrieval (**검색**) — 답에 필요한 문서 골라옴
- **A**ugmented (**증강**) — 그 문서를 프롬프트에 **추가**
- **G**eneration (**생성**) — 보강된 프롬프트로 답 생성

> **핵심은 "찾는 행동" 이 아니라 "프롬프트에 같이 넣는 패턴".**
> 찾는 건 누가 하든 (코드 / Agent) 무방 — RAG 의 본질은 **주입**.

---

# 잠깐 — RAG vs Agent ?

**서로 다른 축의 개념. 대립 X.**

|  | RAG | Agent |
|---|---|---|
| **본질** | 답 전에 외부 정보 같이 주는 **패턴** | LLM 이 언제/뭘 할지 정하는 **루프** |
| **누가 결정?** | 코드가 "검색 먼저" 박음 | LLM 이 "검색할지" 스스로 |
| **루프?** | ❌ 1-pass | ✅ tool → 결과 → 다시 LLM |

**비유**
- **RAG** = 시험 때 책상 위에 자료 깔아두기
- **Agent** = 학생이 "이건 자료 봐야겠다" 스스로 판단

---

# Grounding — `system_instruction` 한 줄

```python
SYSTEM_INSTRUCTION_TEMPLATE = (
    "당신은 사내 노트 검색 도우미입니다. "
    "아래 [관련 노트] 의 내용에만 근거해서 답하세요. "
    "없는 내용은 추측하지 말고 '문서에 없습니다' 라고 답하세요.\n\n"
    "=== 관련 노트 ===\n{context}"
)
```

- 코드가 `retrieve(query)` 로 검색 → `{context}` 자리에 결과 채움
- LLM 은 그 노트 안에서만 답 — 추측 못 함, 출처에 묶임

---

# Retrieval — vector 도 만들자

지금 `retrieve(query)` = **키워드 매칭** (`in` 으로 단어 포함)
- 한계: "쉬는 날" 로 물어보면 "연차" 적힌 문서를 못 찾음 (다른 단어니까)

**오늘 만들 것 — `retrieve_vector(query)`**:
1. 텍스트 → **embedding** (vector, 차원 768+)
2. 노트 7개 미리 embedding → `note_db` (in-memory) 에 저장
3. 질문도 embedding → 모든 노트와 **cosine 유사도** 비교 → top-k

(실무는 Chroma · Pinecone · pgvector 같은 vector DB. 원리는 동일.)

---

# 두 retriever 비교 — 골격은 똑같음

| | `retrieve` (keyword) | `retrieve_vector` (vector) |
|---|---|---|
| 매칭 기준 | 단어 일치 | **의미** 유사도 |
| "쉬는 날" 검색 | "쉬는 날" 있는 문서만 | "연차" 있는 문서도 찾음 |
| 인덱스 | 없음 (매번 스캔) | `note_db` (in-memory) |
| 비용 | 0 | embedding API |

**바뀌는 곳**: 함수 본문 (`retrieve` → `retrieve_vector`) 뿐
**그대로**: `system_instruction` grounding · `rag_answer()` 흐름

> **R-A-G 골격은 똑같음.**
> `rag_answer()` 안의 `retrieve(question)` → `retrieve_vector(question)` 한 줄만 바꾸면 vector RAG 완성.

---

# Vector RAG 실측 — keyword 못 잡고 vector 잡음

```python
def rag_answer_vector(question: str) -> str:
    results = retrieve_vector(question)   # ★ 한 줄만 변경
    context = "\n\n".join(f"# {r['filename']}\n{r['text']}" for r in results)
    ...
```

같은 질문 `"신입사원이 쉬는 날 얼마나 쓸 수 있어?"` 비교:

| | retrieve (keyword) | retrieve_vector (vector) |
|---|---|---|
| 매칭 | "쉬는 날" 단어 → 0건 | 의미상 가까운 `policy_leave.md` 등 |
| RAG 답 | "문서에 없습니다" | 입사 후 6개월 동안 월 1일씩 부여 |

> **retriever 만 교체 = RAG 답이 살아남.**

---

<!-- _class: lead -->

# 🔗 Part 2 — LangChain / LangGraph

W1 Agent + W2 RAG 한 번에 wrap

`week2.ipynb` — Part 2

---

# LangChain vs LangGraph — 누가 뭐 하는가

| | **LangChain** | **LangGraph** |
|---|---|---|
| 역할 | LLM · 도구 · 프롬프트 **추상화 부품** | agent / workflow 의 **state machine** |
| 비유 | 드라이버 · 나사 | 그 부품들로 조립한 **조립도** |
| 우리 코드 | `ChatGoogleGenerativeAI`, `@tool` | `create_react_agent`, `StateGraph` |

> **LangChain** = LLM 호출 wrap
> **LangGraph** = 노드 + 엣지로 state 흘리는 실행 엔진

직접 짠 ~70줄 골격 (W1 Agent + W2 RAG) 을 **한 줄 wrapper** 로 묶을 차례.

---

# LangChain — 부품 (LLM + 도구 등록)

```python
@tool
def find_notes(query: str) -> list[dict]:
    """notes 검색 (vector)."""
    return retrieve_vector(query, top_k=3)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", ...)
resp = llm.invoke([SystemMessage(...), HumanMessage(...)])
```

- `@tool` 1줄 → JSON 스키마 자동 (시그니처 + docstring)
- `llm.invoke(messages)` → LLM 호출 (Gemini SDK wrap)

> **도구는 등록만**. LLM 이 자동 호출 X — `for turn in range(...)` 직접 짜야.
> = LangChain 단독으론 W1 의 `agent_loop` 못 만듦.

---

# LangGraph — 부품 굴리기 (Agent)

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools=[find_notes], prompt=AGENT_PROMPT)
agent.invoke({"messages": [("user", "신입사원 연차?")]})
```

- `create_react_agent` 1줄 = **agent loop state machine** (prebuilt)
- LangChain 의 `llm` + `@tool` 을 LangGraph 가 받아서 굴림 → 도구 호출 / 루프 / 메시지 누적 자동

> **~70줄 → ~5줄.** LangChain 부품을 LangGraph 가 자동화.

---

# 왜 `StateGraph` ? — 실무 시나리오

단순 RAG (`retrieve → generate`) 만이면 함수 한 개로 충분.
LangGraph 진가 = 흐름 복잡할 때.

```
[질문]
  ↓
[retrieve] → "결과 충분?" → No → [웹검색] → 합치기
  ↓ Yes                                ↓
[generate] ← ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ┘
  ↓
[사람 검수 대기]
  ↓
[최종 답]
```

**조건부 분기 / 루프 / HITL / 체크포인트 / 병렬** — 함수 chain 으론 if·else + recursion 지옥.

---

# 한 발 더 — `StateGraph` 직접 짜기

```python
class RAGState(TypedDict):
    question: str; context: str; answer: str

def retrieve_node(state): ...  # → context
def generate_node(state): ...  # → answer

graph = StateGraph(RAGState)
graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)
rag_workflow = graph.compile()
```

> 노드 + 엣지로 `retrieve → generate` workflow 를 명시.

---

# Agent vs Workflow — 둘 다 LangGraph

| | `create_react_agent` | `StateGraph` |
|---|---|---|
| 형태 | **Agent** — LLM 이 흐름 결정 | **Workflow** — 코드가 흐름 정의 |
| 쓸 때 | 자유로운 멀티턴 | 정해진 단계 (RAG · 검수) |

> RAG 처럼 흐름 정해진 건 `StateGraph` 가 명시적.
> 자유 멀티턴은 `create_react_agent`. 실무에선 둘 다 섞어 씀.

---

# 오늘 핵심 한 줄씩

1. **RAG** = `retrieve` / `retrieve_vector` + `system_instruction` 으로 노트에 grounding (할루시네이션 차단)
2. **keyword vs vector**: 단어 매칭 → 의미 매칭. R-A-G 골격은 동일, retriever 만 교체
3. **LangChain / LangGraph** = Agent + RAG 골격을 `create_react_agent` 한 줄로 wrap

**핵심 = "골격" + 그 위에 retriever / 프레임워크 한 줄씩.**

---

<!-- _class: lead -->

# 핵심 메시지

> "오늘 본 게 곧 **에이전트의 전부**.
>
> LangChain / LangGraph 는 우리 골격 위의 표준 wrapper,
> retriever 만 바꾸면 RAG 종류도 바뀜.
>
> **실무 자동화 = 같은 골격 + 회사에 맞는 도구.**"
