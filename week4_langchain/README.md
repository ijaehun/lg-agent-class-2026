# Week 4 — LangChain

이번 주 메시지는 단 하나:

> **W3 에 직접 짠 rag.py 100줄 = LangChain `create_react_agent` 한 줄.**
>
> LangChain 은 우리 골격 위의 **편의 기능**. 본질은 같아요.

W1~W3 에서 노트 검색 도우미를 직접 짰어요. 같은 일을 LangChain 으로 다시 — **줄 단위 비교**.

## 이번 주에 배우는 것

- LangChain (정확히는 LangGraph) 의 `create_react_agent` 사용법
- `@tool` 데코레이터로 도구 등록 — `tool_declarations` 안 쓰는 이유
- `prompt` 인자로 system_instruction 전달
- 우리 코드와 LangChain 코드의 **줄 단위 비교**

## 회차 끝나면 답할 수 있어야 하는 질문

1. `create_react_agent` 한 줄 안에서 일어나는 일을 **본인 입으로** 설명할 수 있는가?
   (= while 루프 / function_call 처리 / function_response 형식 / MAX_TURNS … W3 에 짠 것 전부)
2. 우리가 직접 짠 `rag.py` 와 LangChain 버전의 **차이** 는 어디인가?
3. LangChain 을 쓰면 좋은 상황 / 우리가 직접 짜면 좋은 상황은?
4. Copilot 한테 LangChain agent 짜달라고 했을 때, 답이 옳은지 평가할 수 있는가?

→ 1번이 가장 중요. **"한 줄 안의 정체" 를 알아야 LangChain 을 진짜 쓰는 것**.

---

## 무엇을 만들 건가

W3 의 `rag.py` 와 **완전히 동일한 결과** — LangChain 으로.

같은 노트 폴더, 같은 도구 (`search_notes`), 같은 system_instruction, 같은 사용자 질문 — 결과 동일. **줄 수만 100 → 30.**

사용 예시 (W3 와 동일):
```
You: 신입사원인데 연차 언제부터 쓸 수 있어?
[LangChain agent 가 알아서 search_notes("연차 신입") 호출]
[검색 결과: policy_leave.md, onboarding.md]
답변: 신입사원은 입사 후 6개월 동안 월 1일씩 연차 부여받습니다. (출처: policy_leave.md)
```

차이? **W3 의 100줄이 한 줄로 됨.**

## 어떻게 접근하나 — 바이브 코딩 사고법

### 단계별 사고

**1. 내가 뭘 만들 건가?**
W3 와 똑같은 결과. 다만 우리 골격 대신 LangChain 추상화 사용.

**2. LangChain 이 우리 대신 해주는 게 뭔가?**
- LLM 호출 → `ChatGoogleGenerativeAI`
- 도구 등록 → `@tool` 데코레이터로 자동 스키마 생성 (W3 의 `tool_declarations` 불필요!)
- function_call 처리 → `create_react_agent` 안에서 자동
- while 루프 → 자동
- function_response 형식 → 자동
- MAX_TURNS → 기본값 있음
- system_instruction → `prompt` 인자로 전달

→ W3 에 한 줄씩 짠 모든 것이 **자동화** 됨.

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
`result["messages"]` 를 출력하면 LLM 의 모든 turn / 도구 호출 / 결과가 보임. W3 에 print 로 찍던 것 = LangChain 의 messages.

---

## 직접 해야 하는 것

### (1) 손으로 짜보기 — `langchain_agent.py`

```bash
cd week4_langchain
python langchain_agent.py
```

TODO 두 개:
- 도구 함수 위 `@tool` 데코레이터
- `agent = create_react_agent(llm, tools=[...], prompt=...)` 한 줄

실행하면 W3 rag.py 와 똑같은 답이 나옵니다.

### (2) `rag.py` ↔ `langchain_agent.py` 줄 단위 비교

두 파일을 나란히 열고 **무엇이 사라졌는지** 직접 확인:

| W3 rag.py | W4 langchain_agent.py |
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

**좋은 프롬프트**:
```
LangChain (LangGraph) 의 create_react_agent 로 사내 노트 검색 agent 를 짜줘.

요구사항:
- LLM: langchain_google_genai.ChatGoogleGenerativeAI, gemini-2.5-flash
- 도구: search_notes(keyword) — notes/ 폴더의 .md 파일에서 키워드 검색, @tool 데코레이터
- system prompt: "사내 노트 검색해서 답하라, 결과에 없으면 '문서에 없습니다'"
- 사용자 질문: "신입사원 연차 정책 알려줘"
- result["messages"] 출력으로 전체 흐름 확인
```

### (5) Copilot 답 평가하기 — 체크리스트

- [ ] `@tool` 데코레이터 있는가?
- [ ] `ChatGoogleGenerativeAI` 로 Gemini?
- [ ] `create_react_agent(llm, tools=[...], prompt=...)` 패턴?
- [ ] `agent.invoke({"messages": [...]})` 형식?
- [ ] 결과 출력이 messages 리스트 순회?

→ 옳다면 우리 솔루션과 거의 동일할 것. 차이가 있다면 왜 다른지 토론.

---

## 회차 후 본인 적용

W3 에서 만든 본인 도구를 LangChain 으로:

```python
@tool
def my_business_tool(query: str) -> ...:
    """내 업무 도구 설명"""
    ...

agent = create_react_agent(llm, tools=[my_business_tool], prompt="...")
```

→ "직접 짠 골격이든 LangChain 이든, 도구 자리에 본인 거 넣으면 본인 에이전트".

---

## 핵심 메시지 한 줄

> **`create_react_agent(llm, tools=[...], prompt=...)` 한 줄 안에 W3 의 100줄이 들어있어요.**
> LangChain 의 가치 = 추상화. 우리 가치 = 그 추상화의 정체를 안다는 것.
> 다음 주 (W5 MCP) = 도구 자리를 표준 단자로 바꾸는 것.
