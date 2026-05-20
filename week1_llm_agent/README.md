# Week 1 — LLM + 에이전트 (+ RAG 맛)

3주짜리 강의의 시작. **오늘 한 회차 (4시간) 안에** LLM 호출부터 에이전트 + RAG 맛까지 다 갑니다.

> **Part 1**: LLM 한 번 호출 + 한계 발견 (`hello.py`, `chat.py`)
> **Part 2**: 도구 도입 = 에이전트 + Skill 추가 (`tool_use.py`, `agent_loop.py`, `agent_skill.py`)

## 이번 주에 배우는 것

- `client.models.generate_content(...)` 한 줄로 Gemini 부르기
- **LLM 만으론 내 노트에 답할 수 없다** 는 한계 발견 (Part 1 클라이맥스)
- LLM 응답이 **텍스트 대신 function_call** 일 수 있다는 것
- 도구 호출 4단계 + `while` 루프 = **에이전트**
- 도구 한 개 더 추가 (`search_notes`) = **이게 곧 RAG**

## 회차 끝나면 답할 수 있어야 하는 질문

1. LLM 한 번 호출하는 **핵심 한 줄** 은?
2. LLM 이 직전 대화를 기억하나? 아니라면 멀티턴은 어떻게?
3. **"내 회의록 요약해줘" 라고 물으면 LLM 이 어떻게 답하나? 왜?** (Part 1 핵심)
4. LLM 이 "함수를 호출했다" 는 게 무슨 뜻인가?
5. `while` 루프가 왜 필요한가?
6. **에이전트 = ? + ? + ?** (한 줄로)
7. RAG 와 일반 에이전트의 차이는 코드 어디인가?

→ 마지막에 본인 입에서 자연스럽게 나오면 성공.

---

## 3주 전체 시나리오 — 매주 같은 에이전트가 더 똑똑해짐

| 주차 | 에이전트가 무엇을 할 수 있나 |
|---|---|
| **W1 (오늘)** | LLM 호출 → 도구 → 에이전트 → **RAG 맛까지** |
| W2 | RAG 심화 (system_instruction) + **LangChain 한 줄로** |
| W3 | **MCP** 표준으로 도구 노출 (Claude Desktop 에서 직접 사용) |

→ **회차마다 도구만 추가 / 표준화**. 골격 (LLM + 도구 + 루프) 은 끝까지 동일.

---

## 무엇을 만들 건가

| 파일 | 역할 |
|---|---|
| `hello.py` | 한 줄짜리 Gemini 응답 받기 |
| `chat.py` | 멀티턴 대화 챗봇 (history 누적) |
| `tool_use.py` | 도구 호출 한 턴 (4단계) |
| `agent_loop.py` | 도구 2개 + while 루프 = 에이전트 |
| `agent_skill.py` | 도구 한 개 더 (`search_notes`) = RAG |

---

# 📘 Part 1 — LLM 다루기

## 어떻게 접근하나 — 바이브 코딩 사고법

**1. 내가 뭘 만들 건가?** 사용자 입력 → LLM → 응답 출력.

**2. 어떤 구조?**
```
입력 (prompt) → LLM API → 응답 (text)
```
세 가지 결정만: 어떤 모델, 무엇을 보낼지, 응답에서 무엇을 꺼낼지.

**3. 한 번에 끝나나?** hello.py 는 한 번. chat.py 는 여러 턴 → 반복.

**4. 멀티턴은 어떻게?** LLM 은 직전 대화를 기억 못 함. 우리가 매번 **전체 대화를 다시 보내야** 함 (history 리스트).

**5. 한계는?**
- 토큰 한계 (history 가 너무 길면 못 받음)
- **사내 정보를 모름** ← Part 1 의 핵심 발견. Part 2 에서 해결.

## 직접 해야 하는 것 — Part 1

### (1) 손으로 짜보기 — `hello.py`

```bash
cd week1_llm_agent
python hello.py
```

TODO (1) 채우기. 첫 시도는 단순 질문 ("자기소개").

### (2) ★ LLM 의 한계 직접 체감하기

`hello.py` 의 `contents` 를 다음으로 바꿔서 실행:

```python
contents="이번 주 우리 팀 회의록을 한 줄로 요약해줘"
```

→ LLM 이 뭐라고 답하나요?
- "회의록 내용을 알 수 없습니다" 라고 정직하게? (좋은 경우)
- 또는 그럴듯하게 추측해서 만들어낸 답? (할루시네이션 — 위험!)

→ **`notes/` 폴더에 진짜 회의록 파일이 있는데도** LLM 은 그걸 못 봅니다.
**Part 2 = 이 한계를 도구로 해결.**

### (3) 손으로 짜보기 — `chat.py`

멀티턴 대화 — history 누적.

```bash
python chat.py
```

TODO 두 개: user / model 입력을 history 에 추가.

### (4) 망가뜨려보기 — "왜 history 가 필요한가"

`history.append` 두 줄을 주석 처리하고 다시 실행:

```
You: 내 이름은 영희야
Model: 반가워요!
You: 내 이름이 뭐였지?
Model: 죄송하지만 이름을 알려주신 적 없어요.   ← history 없으면 기억 못 함
```

→ **LLM 이 stateless** 라는 본질. 우리 코드가 매번 history 를 다시 보내야 LLM 이 "기억하는 척" 가능.

### (5) Copilot 한테 시켜보기

빈 파일 `my_chat.py` 만들고 Copilot 에:

```
Python 으로 Gemini 멀티턴 챗봇을 짜줘.

요구사항:
- google.genai SDK 사용
- .env 에서 GEMINI_API_KEY 로드
- history 리스트에 user/model 턴 누적, 매번 contents 로 전체 전달
- "exit" 또는 빈 줄로 종료
- 모델: gemini-3.5-flash
```

체크리스트:
- [ ] `history` 리스트가 있는가?
- [ ] 매 턴마다 **누적** 되는가? (덮어쓰지 않고)
- [ ] `contents=history` 로 전체를 보내는가?
- [ ] role 이 `"user"` / `"model"` 형식 맞는가?
- [ ] 종료 조건이 있는가?

---

# 🔧 Part 2 — 에이전트 + Skill 추가

> Part 1 에서 발견한 한계 (**LLM 이 내 노트를 모름**) 를 **도구로** 해결.
> **이 회차가 강의 전체에서 가장 중요.**

## 어떻게 접근하나 — 바이브 코딩 사고법

**1. 내가 뭘 만들 건가?** 사용자 질문 → 시스템이 알아서 노트 읽고 답.

**2. 어떤 구조?**
LLM 혼자선 노트 못 읽음. 그래서 우리 Python 코드가 노트 읽어주는 **도구** 필요.
```
사용자 → LLM → (도구 호출 요청) → 우리 코드 (read_note) → 결과 → LLM → 사용자
```

**3. 한 번에 끝나나?**
"가장 최근 회의록 요약" 같은 질문엔 도구 두 번 (list → read) 필요. → **반복 (while)**.

**4. 언제 멈추나?** LLM 이 도구 안 부르고 **자연어 텍스트로 답할 때** = 끝.

**5. 안전장치?** LLM 이 무한히 도구만 부르면? → `MAX_TURNS` 상한.

## 직접 해야 하는 것 — Part 2

### (1) 손으로 짜보기 — `tool_use.py`

도구 호출 **한 턴** 의 4단계 흐름 손에 익히기.

```bash
python tool_use.py
```

기본 질문: `"policy_leave.md 파일 내용을 한 줄로 요약해줘"`

TODO 두 개:
- `read_note(**function_call.args)` — 도구 실제 실행
- `function_response` 형식의 dict — LLM 에 결과 돌려주기

**생각해볼 거리**:
- `**` 두 개의 의미는?
- `function_response` 의 role 이 왜 `"user"` 일까?

### (2) ★ 망가뜨려보기 — "왜 이렇게 짜야 하는지"

| 망가뜨릴 곳 | 예상 결과 |
|---|---|
| `function_response` 의 dict 를 평범한 텍스트로 | LLM 이 결과 못 알아듣고 다시 호출 |
| `read_note_declaration` 의 description 빈 문자열 | LLM 이 도구를 안 부르거나 잘못 부름 |
| `read_note` 함수가 `return ""` | LLM 이 "내용을 알 수 없습니다" 답 |

각 망가뜨림 후 "무슨 일이 일어났는지" 한 줄로 정리. **이게 진짜 학습.**

### (3) 손으로 짜보기 — `agent_loop.py`

도구 2개 (`list_notes`, `read_note`) + while 루프.

```bash
python agent_loop.py
```

기본 질문: `"가장 최근 회의록 한 줄로 요약해줘"` — LLM 이 list → read 순서로 도구 호출.

TODO 두 개:
- 종료 조건 (function_call 없으면 break)
- 도구 라우팅 (TOOL_FUNCTIONS dict)

### (4) ★ Skill 추가 — `agent_skill.py` (강의 클라이맥스)

> "도구 하나 더 끼우면 능력이 늘어난다" 를 직접 확인.

`agent_loop.py` 골격은 **안 건드림**. 도구 (`search_notes`) 한 개 더 등록만:

```bash
python agent_skill.py
```

기본 질문: `"신입사원인데 연차 언제부터 쓸 수 있어?"`
→ LLM 이 `search_notes("연차")` 부름 → `policy_leave.md` 발견 → `read_note` → 답.

TODO 두 개:
- `TOOL_FUNCTIONS` 에 `search_notes` 등록 (1줄)
- `search_notes_declaration` 작성 (한 덩어리 — `read_note` 구조 참고)

**생각해볼 거리**:
- `agent_loop.py` 와 `agent_skill.py` 의 **다른 줄이 몇 줄?** (도구 추가분만)
- → "**에이전트 골격은 안 변함. 도구만 추가.**" 이게 강의의 핵심.

**그리고 — 이게 곧 RAG (Retrieval-Augmented Generation).**
검색해서 (Retrieval) 그 결과를 LLM 한테 줘서 (Augmented) 답을 만든다 (Generation).
**거창한 이름이지만, 에이전트 골격에 `search_notes` 라는 도구 하나 추가한 것뿐.**

### (5) Copilot 한테 시켜보기 — 같은 에이전트

빈 파일 `my_agent.py` 만들고 Copilot 에:

```
Python 으로 LLM agent loop 를 짜줘.

요구사항:
- google.genai SDK 사용
- 도구 두 개:
  - list_notes() -> list[str]: notes/ 폴더의 .md 파일 목록
  - read_note(filename) -> str: notes/<filename> 의 내용
- 사용자 질문 받아 LLM 이 도구 부르고 결과 보면 또 부를 수 있게 while 루프
- LLM 이 텍스트로 답하면 종료
- MAX_TURNS = 5 안전장치
- function_response 형식 표준 따르기
```

체크리스트:
- [ ] `while` 루프 있는가? 종료 조건은?
- [ ] `function_call` 이 없을 때 어떻게 처리?
- [ ] `function_response` 형식이 우리 코드와 같은가?
- [ ] `MAX_TURNS` 안전장치 있는가?
- [ ] 도구 두 번 호출되는 시나리오가 잘 동작?

차이가 있다면 우리 솔루션과 비교 — **어느 게 더 나은가? 왜?**

---

## 회차 후 본인 적용 (W2 준비)

오늘 만든 30~40줄이 RAG 의 전부. 다음 주 (W2) 에서 같은 일을 **LangChain `create_react_agent` 한 줄로** 다시 짭니다.

> "내 업무에서 '검색 → 읽기 → 답변' 형태로 자동화하고 싶은 게 무엇?"

한 줄로 메모해두세요. W2 의 재료가 됩니다.

---

## 핵심 메시지 두 줄

> 1. **`client.models.generate_content(model=, contents=)` 한 줄이 LLM 호출의 본질.**
>    RAG / LangChain / MCP 까지 가도 이 한 줄은 그 자리에.
>
> 2. **에이전트 = LLM + 도구 + 반복 루프. 그게 전부.**
>    여러분이 손으로 짠 30~40줄이 RAG 의 전부 — LangChain · MCP 는 그 위의 변형.
