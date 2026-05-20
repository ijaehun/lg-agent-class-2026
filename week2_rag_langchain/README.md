# Week 2 — RAG 심화 + LangChain

W1 에서 만든 `agent_skill.py` (= RAG 의 기본형) 를 두 단계로 발전:

> **Part 1**: RAG 심화 — `system_instruction` 으로 grounding (할루시네이션 방지) (`rag.py`, `notes_agent.py`)
> **Part 2**: 같은 일을 **LangChain 한 줄로** — `create_react_agent` (`langchain_agent.py`)

## 이번 주에 배우는 것

- **RAG** 의 본질 다시 — Retrieval + Augmented Generation
- `system_instruction` 으로 LLM 답변 행동 제약 (할루시네이션 방지)
- 도구 3개 (`list_notes`, `read_note`, `search_notes`) 협업 패턴
- LangChain 의 `create_react_agent` — W1 의 30~40줄이 **한 줄로**
- `@tool` 데코레이터로 도구 등록 (`tool_declarations` 자동)
- **우리 골격 ↔ LangChain** 줄 단위 비교

## 회차 끝나면 답할 수 있어야 하는 질문

1. W1 의 `agent_skill.py` 와 `rag.py` 의 차이를 코드로 짚을 수 있는가? (`system_instruction` 한 줄)
2. `system_instruction` 이 없으면 LLM 이 어떻게 답할까?
3. `create_react_agent` **한 줄 안에서 일어나는 일** 을 본인 입으로 설명할 수 있는가?
   (= while 루프 / function_call 처리 / function_response / MAX_TURNS — W1 에서 짠 것 전부)
4. LangChain 을 쓰면 좋은 상황 / 직접 짜면 좋은 상황은?
5. Copilot 한테 LangChain agent 짜달라고 했을 때, 답이 옳은지 평가할 수 있는가?

→ 3번이 가장 중요. **"한 줄 안의 정체" 를 알아야 LangChain 을 진짜 쓰는 것.**

---

## 3주 시나리오 — 지금 어디?

| 주차 | 무엇 |
|---|---|
| W1 | LLM + 에이전트 + RAG 맛 (`agent_skill.py` 까지) |
| **W2 (오늘)** | **RAG 심화 + LangChain** — `system_instruction`, `create_react_agent` |
| W3 | MCP 표준 — 도구를 표준 단자로 노출 |

→ **회차마다 도구는 그대로. 추상화/표준화만 추가.**

---

## 무엇을 만들 건가

| 파일 | 역할 |
|---|---|
| `rag.py` | RAG 의 본질 — `search_notes` + `system_instruction` grounding |
| `notes_agent.py` | 실전 — 도구 3개 (list + read + search) 통합 |
| `langchain_agent.py` | 같은 일을 **LangChain 한 줄로** |

---

# 📘 Part 1 — RAG 심화

> W1 의 `agent_skill.py` 는 검색해서 답하지만, **할루시네이션은 막을 수 없음**.
> Part 1 = `system_instruction` 으로 "검색 결과에만 근거" 강제 + 도구 3개 협업.

## 어떻게 접근하나

**1. 뭘 만들 건가?** LLM 이 모르는 정보 (내 노트) 를 **검색해서 그 내용에 근거해 답** 하는 에이전트.

**2. 어떤 구조?**
W1 agent_skill 골격 그대로. `system_instruction` 한 줄 추가.
```
[W1 agent_skill]:  tools = [list, read, search]
[W2 rag.py]:       tools = [search] + system_instruction
[W2 notes_agent.py]: tools = [list, read, search] + system_instruction
```

**3. 검색 결과를 LLM 한테 어떻게 줄까?**
W1 의 `function_response` 형식 그대로. 도구 결과 형식은 무엇이든 OK.

**4. LLM 이 검색 결과에 근거해 답하게 강제할 방법?**
`system_instruction` — "반드시 search 로 먼저 검색하고, 결과에 없는 내용은 추측 마라" 한 문장.

**5. 본인 업무에선?**
도구 함수 안의 구현만 바꿈 (사내 API, 슬랙 검색 등). 골격 동일.

## 직접 해야 하는 것 — Part 1

### (1) 손으로 짜보기 — `rag.py`

```bash
cd week2_rag_langchain
python rag.py
```

TODO 두 개:
- 검색 점수 계산 (`score = sum(...)`)
- `SYSTEM_INSTRUCTION` 작성 (할루시네이션 방지)

**생각해볼 거리**:
- 점수가 0 인 문서는 왜 제외?
- `SYSTEM_INSTRUCTION` 이 없으면 LLM 이 검색 안 하고 추측해서 답할 수도.

### (2) `agent_skill.py` (W1) ↔ `rag.py` 비교

두 파일 나란히 열고 diff 처럼. **다른 줄 몇 줄?**
- 도구 함수 추가 안 함 — 이미 W1 에 있음
- `system_instruction` 추가 — **이 한 줄이 RAG 심화의 정체**
- agent loop 30줄: **완전 동일**

→ "에이전트 골격은 그대로" 가 W1 에 이어 다시 한 번 눈으로.

### (3) 망가뜨려보기

| 망가뜨릴 곳 | 예상 결과 |
|---|---|
| `SYSTEM_INSTRUCTION` 빈 문자열 | LLM 이 검색 안 하고 추측해서 답할 수도 |
| `search_notes` description 빈 문자열 | LLM 이 도구를 안 부름 |
| `search_notes` 가 빈 리스트만 반환 | LLM 이 "문서에 없습니다" 라고 답해야 옳음 — 실제 그런지 확인 |

### (4) 실전 — `notes_agent.py`

도구 3개 통합. 본인 폴더로 NOTES_DIR 지정 가능:

```powershell
# Windows — 기본 (강의 notes/)
python notes_agent.py

# Windows — 본인 폴더
$env:NOTES_DIR="C:\본인\문서폴더"; python notes_agent.py

# macOS
NOTES_DIR=/Users/본인/문서폴더 python3 notes_agent.py
```

TODO 1 개:
- `TOOL_FUNCTIONS` 딕셔너리 — 도구 3개 라우팅

질문 예시:
- "출장비 정산은 어떻게 해?" → search_notes 호출
- "policy_remote.md 보여줘" → read_note 호출
- "내 노트에 뭐가 있어?" → list_notes 호출

LLM 이 알아서 적절한 도구 고름.

---

# 🔗 Part 2 — LangChain 한 줄로

> Part 1 에서 짠 100줄 = LangChain `create_react_agent` **한 줄**.
> LangChain 은 우리 골격 위의 **편의 기능**. 본질은 같음.

## 어떻게 접근하나

**1. 뭘 만들 건가?** Part 1 과 똑같은 결과. 다만 우리 골격 대신 LangChain 추상화 사용.

**2. LangChain 이 우리 대신 해주는 게 뭔가?**
- LLM 호출 → `ChatGoogleGenerativeAI`
- 도구 등록 → `@tool` 데코레이터로 자동 스키마 생성 (`tool_declarations` 불필요!)
- function_call 처리 → `create_react_agent` 안에서 자동
- while 루프 → 자동
- function_response 형식 → 자동
- MAX_TURNS → 기본값 있음
- system_instruction → `prompt` 인자로 전달

→ Part 1 에 한 줄씩 짠 모든 것이 **자동화**.

**3. 그럼 LangChain 만 쓰면 되지 왜 직접 짰나?**
- 우리가 한 번 짜봤기 때문에 **LangChain 안에서 무슨 일이 일어나는지** 알 수 있음
- 디버깅 / 커스터마이징 때 결정적 차이
- Copilot 한테 시켜도 답이 옳은지 평가 가능

**4. 어떻게 LangChain 코드를 짜나?**
- 도구 함수 위에 `@tool` 데코레이터
- LLM 인스턴스 (`ChatGoogleGenerativeAI`)
- `create_react_agent(llm, tools=[...], prompt=SYSTEM_PROMPT)` 한 줄
- `agent.invoke({"messages": [("user", "질문")]})` 로 실행

**5. 디버깅은?**
`result["messages"]` 를 출력하면 LLM 의 모든 turn / 도구 호출 / 결과가 보임. Part 1 에 print 로 찍던 것 = LangChain 의 messages.

## 직접 해야 하는 것 — Part 2

### (1) 손으로 짜보기 — `langchain_agent.py`

```bash
python langchain_agent.py
```

TODO 두 개:
- 도구 함수 위 `@tool` 데코레이터
- `agent = create_react_agent(llm, tools=[...], prompt=...)` 한 줄

실행하면 Part 1 `rag.py` 와 똑같은 답.

### (2) ★ `rag.py` ↔ `langchain_agent.py` 줄 단위 비교

두 파일 나란히 열고 **무엇이 사라졌는지** 직접 확인:

| Part 1 rag.py | Part 2 langchain_agent.py |
|---|---|
| `tool_declarations` (15줄) | `@tool` 데코레이터 (1줄) |
| `TOOL_FUNCTIONS` 딕셔너리 | 없음 (자동) |
| `for turn in range(MAX_TURNS)` 루프 | 없음 (자동) |
| `function_calls = [p.function_call for ...]` | 없음 (자동) |
| `if not function_calls: break` 종료 조건 | 없음 (자동) |
| `tool_response_parts.append(...)` | 없음 (자동) |
| `history.append({"role": "user", ...})` | 없음 (자동) |
| `system_instruction=` (config 안에) | `prompt=` (create_react_agent 인자) |

**100줄 → 30줄, 핵심 한 줄 = `create_react_agent`.**

### (3) 망가뜨려보기 — LangChain 도 똑같이 동작 안 함

| 망가뜨릴 곳 | 예상 결과 |
|---|---|
| `@tool` 데코레이터 제거 | `create_react_agent` 가 도구 인식 못 함 |
| docstring 빈 문자열 | LLM 이 도구가 뭐 하는지 몰라 안 부르거나 잘못 부름 |
| `prompt=` 빼기 | LLM 이 검색 안 하고 추측해서 답할 수도 (할루시네이션) |

→ "LangChain 도 결국 약속된 형식 위에서 동작" 이라는 본질 체감.

### (4) Copilot 한테 시켜보기 — 같은 일 LangChain 으로

빈 파일 `my_lc_agent.py` 만들고 Copilot 에:

```
LangChain (LangGraph) 의 create_react_agent 로 사내 노트 검색 agent 를 짜줘.

요구사항:
- LLM: langchain_google_genai.ChatGoogleGenerativeAI, gemini-3.5-flash
- 도구: search_notes(keyword) — notes/ 폴더의 .md 파일에서 키워드 검색, @tool 데코레이터
- system prompt: "사내 노트 검색해서 답하라, 결과에 없으면 '문서에 없습니다'"
- 사용자 질문: "신입사원 연차 정책 알려줘"
- result["messages"] 출력으로 전체 흐름 확인
```

체크리스트:
- [ ] `@tool` 데코레이터 있는가?
- [ ] `ChatGoogleGenerativeAI` 로 Gemini?
- [ ] `create_react_agent(llm, tools=[...], prompt=...)` 패턴?
- [ ] `agent.invoke({"messages": [...]})` 형식?
- [ ] 결과 출력이 messages 리스트 순회?

→ 옳다면 우리 솔루션과 거의 동일할 것. 차이가 있다면 왜 다른지 토론.

---

## 회차 후 본인 적용

본인 도구를 LangChain 으로:

```python
@tool
def my_business_tool(query: str) -> ...:
    """내 업무 도구 설명"""
    ...

agent = create_react_agent(llm, tools=[my_business_tool], prompt="...")
```

→ "직접 짠 골격이든 LangChain 이든, 도구 자리에 본인 거 넣으면 본인 에이전트".

다음 주 (W3 MCP) = 이 도구 자리를 **표준 단자** 로 바꾸는 것.

---

## 핵심 메시지 두 줄

> 1. **agent loop 의 도구 자리에 무엇을 넣느냐가 에이전트의 정체.**
>    날씨 → 노트 검색 → 본인 업무. 골격은 그대로.
>
> 2. **`create_react_agent(llm, tools=[...], prompt=...)` 한 줄 안에 우리가 짠 100줄이 들어있다.**
>    LangChain 의 가치 = 추상화. 우리 가치 = 그 추상화의 정체를 안다는 것.
