# Week 4 — LangChain

이번 주 메시지는 단 하나:

> **우리가 W2 에 직접 짠 agent_loop 100줄 = LangChain `create_react_agent` 한 줄.**
>
> LangChain 은 우리 골격 위의 **편의 기능**. 본질은 같아요.

## 이번 주에 배우는 것

- LangChain (정확히는 LangGraph) 의 `create_react_agent` 사용법
- `@tool` 데코레이터로 도구를 등록하는 패턴
- 우리가 짠 코드와 LangChain 코드의 **줄 단위 비교**
- "추상화" 의 의미 — 우리가 W2 에 매번 짠 것을 한 줄로 부르는 것

## 회차 끝나면 답할 수 있어야 하는 질문

1. `create_react_agent` 한 줄 안에서 일어나는 일을 **본인 입으로** 설명할 수 있는가?
   (= while 루프 / function_call 처리 / function_response 형식 / MAX_TURNS … 우리가 W2 에 짠 것 전부)
2. 우리가 직접 짠 agent_loop.py 와 LangChain 버전의 **차이** 는 어디인가?
3. LangChain 을 쓰면 좋은 상황 / 우리가 직접 짜면 좋은 상황은?
4. Copilot 한테 LangChain agent 짜달라고 했을 때, 답이 옳은지 평가할 수 있는가?

→ 1번이 가장 중요. **"한 줄 안의 정체" 를 알아야 LangChain 을 진짜 쓰는 것**.

---

## 무엇을 만들 건가

W2 의 `agent_loop.py` 와 **완전히 동일한 결과** — LangChain 으로.

사용 예시 (W2 와 동일):
```
You: 서울 날씨 보고 오늘 뭐 입을지 추천해줘

[LangChain agent 가 알아서 도구 두 번 호출]
  1. get_weather("서울") → {"temp_celsius": 22, ...}
  2. recommend_outfit(22) → "긴팔 + 청바지"

답변: 서울은 22도 맑네요. 긴팔에 청바지 추천드려요.
```

차이? **agent_loop.py 의 100줄이 한 줄로 됨.**

## 어떻게 접근하나 — 바이브 코딩 사고법

### 단계별 사고

**1. 내가 뭘 만들 건가?**
W2 와 똑같은 결과. 다만 우리가 직접 짠 골격 대신 LangChain 의 추상화를 쓴다.

**2. LangChain 이 우리 대신 해주는 게 뭔가?**
- LLM 호출 → `ChatGoogleGenerativeAI` 가 담당
- 도구 등록 → `@tool` 데코레이터로 자동 스키마 생성
- function_call 처리 → `create_react_agent` 안에서 자동
- while 루프 → 자동
- function_response 형식 → 자동
- MAX_TURNS → 기본값 있음

→ 우리가 W2 에 한 줄씩 짠 모든 것이 **자동화** 됨.

**3. 그럼 LangChain 만 쓰면 되지 왜 직접 짰나?**
- 우리가 한 번 짜봤기 때문에 **LangChain 안에서 무슨 일이 일어나는지** 알 수 있어요
- 디버깅할 때, 커스터마이징할 때 결정적 차이
- Copilot 한테 시켜도 답이 옳은지 평가 가능

**4. 어떻게 LangChain 코드를 짜나?**
- 도구 함수 위에 `@tool` 데코레이터
- LLM 인스턴스 생성 (`ChatGoogleGenerativeAI`)
- `create_react_agent(llm, tools=[...])` 한 줄
- `agent.invoke({"messages": [("user", "질문")]})` 로 실행

**5. 디버깅은?**
`result["messages"]` 를 출력하면 LLM 의 모든 turn / 도구 호출 / 결과가 보임. 우리가 W2 에 print 로 찍던 것 = LangChain 의 messages.

---

## 직접 해야 하는 것

### (1) 손으로 짜보기 — `langchain_agent.py`

```bash
cd week4_langchain
python langchain_agent.py
```

TODO 두 개:
- 도구 함수 위 `@tool` 데코레이터
- `agent = create_react_agent(llm, tools=[...])` 한 줄

실행하면 W2 agent_loop.py 와 똑같은 답이 나옵니다.

### (2) `agent_loop.py` ↔ `langchain_agent.py` 줄 단위 비교

두 파일을 나란히 열고 **무엇이 사라졌는지** 직접 확인하세요:

| W2 agent_loop.py | W4 langchain_agent.py |
|---|---|
| `tool_declarations` (15줄) | `@tool` 데코레이터 (1줄) |
| `TOOL_FUNCTIONS` 딕셔너리 | 없음 (자동) |
| `for turn in range(MAX_TURNS)` 루프 | 없음 (자동) |
| `function_calls = [p.function_call for ...]` | 없음 (자동) |
| `if not function_calls: break` 종료 조건 | 없음 (자동) |
| `tool_response_parts.append(...)` | 없음 (자동) |
| `history.append({"role": "user", "parts": ...})` | 없음 (자동) |

**100줄 → 30줄, 핵심 한 줄 = `create_react_agent`.**

→ "이게 LangChain 의 가치" 가 눈에 들어옵니다.

### (3) 망가뜨려보기 — LangChain 도 똑같이 동작 안 함

| 망가뜨릴 곳 | 예상 결과 |
|---|---|
| `@tool` 데코레이터 제거 | `create_react_agent` 가 도구 인식 못 함 → 에러 또는 LLM 이 도구 안 부름 |
| `recommend_outfit` 의 docstring 빈 문자열 | LLM 이 도구가 뭐 하는지 몰라서 안 부르거나 잘못 부름 |
| `result["messages"]` 대신 `result["output"]` 로 출력 시도 | KeyError — LangChain 의 결과 구조도 약속 |

→ "LangChain 도 결국 약속된 형식 위에서 동작" 이라는 본질 체감.

### (4) Copilot 한테 시켜보기 — 같은 일 LangChain 으로

빈 파일 `my_lc_agent.py` 만들고 Copilot 한테:

**좋은 프롬프트** (위 사고법 기반):
```
LangChain (LangGraph) 의 create_react_agent 로 agent 를 만들어줘.

요구사항:
- LLM: langchain_google_genai.ChatGoogleGenerativeAI, gemini-2.5-flash
- 도구 두 개: get_weather(city), recommend_outfit(temp_celsius) — @tool 데코레이터로
- 사용자 질문: "서울 날씨 보고 옷 추천"
- result["messages"] 출력으로 전체 흐름 보기
```

**나쁜 프롬프트**:
```
LangChain agent 짜줘
```

### (5) Copilot 답 평가하기 — 체크리스트

- [ ] `@tool` 데코레이터 있는가?
- [ ] `ChatGoogleGenerativeAI` 로 Gemini 연결?
- [ ] `create_react_agent(llm, tools=[...])` 패턴?
- [ ] `agent.invoke({"messages": [...]})` 형식 맞는가?
- [ ] 결과 출력이 messages 리스트 순회?

→ Copilot 답이 옳다면 우리 솔루션과 거의 동일할 것. 차이가 있다면 왜 다른지 토론.

---

## 회차 후 본인 적용

**W3 에서 만든 본인 도구를 LangChain 으로 옮겨보기.**

```python
@tool
def my_business_tool(query: str) -> ...:
    """내 업무 도구 설명"""
    ...

agent = create_react_agent(llm, tools=[my_business_tool])
```

→ "직접 짠 골격이든 LangChain 이든, 도구 자리에 본인 거 넣으면 본인 에이전트" 라는 메시지 강화.

---

## 핵심 메시지 한 줄

> **`create_react_agent(llm, tools=[...])` 한 줄 안에 우리가 W2 에 짠 100줄이 들어있어요.**
> LangChain 의 가치 = 추상화. 우리 가치 = 그 추상화의 정체를 안다는 것.
> 다음 주 (W5 MCP) 도 마찬가지 — 도구 자리를 표준 단자로 바꾸는 것.
