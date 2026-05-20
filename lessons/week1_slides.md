---
marp: true
theme: default
paginate: true
size: 16:9
header: 'LG KAMP · AI 에이전트 강의 · W1'
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
  /* W1 flow diagram */
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
  .limit-box {
    padding: 10px 14px;
    background: #fce8e6;
    color: #c5221f;
    border-radius: 8px;
    font-size: 14px;
    font-weight: bold;
    border: 2px dashed #c5221f;
  }
  /* Head + limbs diagram */
  .body-diagram {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    margin: 24px 0;
  }
  .head-box {
    padding: 22px 36px;
    background: #1a73e8;
    color: white;
    border-radius: 60px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    box-shadow: 0 6px 14px rgba(26,115,232,0.35);
  }
  .head-box small {
    display: block;
    font-size: 14px;
    font-weight: normal;
    opacity: 0.9;
    margin-top: 4px;
  }
  .stem {
    width: 3px;
    height: 30px;
    background: linear-gradient(180deg, #1a73e8, #d93025);
  }
  .limbs-row {
    display: flex;
    gap: 14px;
    align-items: center;
    flex-wrap: nowrap;
  }
  .limb-box {
    padding: 12px 16px;
    background: white;
    border: 2px solid #d93025;
    border-radius: 10px;
    text-align: center;
    font-family: 'JetBrains Mono', 'D2Coding', 'Consolas', monospace;
    color: #d93025;
    font-size: 18px;
    font-weight: bold;
    box-shadow: 0 2px 6px rgba(217,48,37,0.15);
    min-width: 130px;
  }
  .limb-box small {
    display: block;
    font-size: 12px;
    color: #777;
    font-family: 'Pretendard', sans-serif;
    font-weight: normal;
    margin-top: 4px;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Week 1
## 나만의 에이전트 만들기

---

# 오늘의 학습 흐름

<div class="week-flow">
  <div class="part-row">
    <div class="part-title">📘 Part 1 — LLM 호출</div>
    <div class="part-sub">API 로 LLM 호출 + 응답 다루기</div>
    <div class="files-row">
      <div class="file-box">
        <span class="file-name">hello.py</span>
        <span class="file-desc">LLM 호출</span>
      </div>
      <div class="arrow">→</div>
      <div class="file-box">
        <span class="file-name">chat.py</span>
        <span class="file-desc">멀티턴</span>
      </div>
    </div>
  </div>

  <div class="part-row">
    <div class="part-title">🔧 Part 2 — 에이전트</div>
    <div class="part-sub">LLM 에 팔다리 (도구) 달기</div>
    <div class="files-row">
      <div class="file-box">
        <span class="file-name">tool_use.py</span>
        <span class="file-desc">도구 1턴</span>
      </div>
      <div class="arrow">→</div>
      <div class="file-box">
        <span class="file-name">agent_loop.py</span>
        <span class="file-desc">+ 루프 = 에이전트</span>
      </div>
      <div class="arrow">→</div>
      <div class="file-box">
        <span class="file-name">agent_skill.py</span>
        <span class="file-desc">도구 확장</span>
      </div>
    </div>
  </div>
</div>

---

# 오늘의 학습 목표

1. LLM API 를 호출해 응답을 받는 기본 패턴은 무엇인가
2. 여러 턴 대화 (챗봇) 는 어떻게 구현하는가
3. LLM 이 함수를 호출한다는 것은 어떤 의미인가
4. 에이전트 루프에서 반복 (`while`) 이 필요한 이유는
5. **에이전트의 핵심 구성 요소 세 가지는 무엇인가**

★ Part 1 (1·2): 로컬에서 LLM 채팅 만들기
★ Part 2 (3~5): 도구를 달아 에이전트로

---

# 본 강의의 학습 방식

**Copilot 만 사용할 때의 문제점**

- 주도적 코드 작성 능력 부재
- 코드 구조에 대한 이해 부족
- Copilot 에 대한 종속

**본 강의의 학습 흐름**

> 구조 이해 → 베이스라인 코드 → Copilot 으로 확장 → 결과 공유

**베이스라인** — 완성 코드 제공
**확장** — 본인 업무에 맞게 (Copilot 활용)

---

<!-- _class: lead -->

# 📘 Part 1 — LLM 호출

`hello.py` + `chat.py`

API 호출로 LLM 응답 받기, 멀티턴 대화 구현

---

# LLM API 호출 — 에이전트의 머리 가져오기

<div class="body-diagram">
  <div class="head-box">LLM<br/><small>머리 — 사고</small></div>
</div>

**Part 1 의 목표** — LLM 을 **API 로 호출해서 사용**

- 사용자 질문 → Gemini API 호출 → LLM 응답
- 여러 턴 대화 (챗봇) 구현

**Part 2 에서** — 팔다리 (도구) 추가

> LLM 이 에이전트의 시작점.

---

# `hello.py` — LLM API 호출

```python
# 1. SDK + .env
from google import genai
from dotenv import load_dotenv
load_dotenv()                       # .env 파일의 API 키를 환경변수로 로드

# 2. 클라이언트 생성 (API 키로 인증)
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 3. ★ LLM 호출 — 핵심 한 줄
response = client.models.generate_content(
    model="gemini-2.5-flash",       # 사용할 모델
    contents="안녕? 자기소개",      # LLM 에 보낼 프롬프트
)

# 4. 응답에서 텍스트만 추출
print(response.text)                # response 객체의 텍스트 필드
```

---

# LLM 은 매 호출 백지 상태 (Stateless)

**LLM 자체의 특성**

- 호출 간 상태 유지 없음
- 직전 대화를 기억하지 않음

> 두 번 따로 호출하면 LLM 은 첫 번째 호출을 모름.
> 챗봇처럼 이어가려면 우리가 history 를 관리해야 함.

---

# `hello.py` 의 한계

- 한 번 묻고 한 번 답하면 종료
- 이전 대화 맥락 유지 불가

**목표** — 멀티턴 대화

> 매번 누적된 history 를 다시 전송 → `chat.py`

---

# `chat.py` — history 누적

```python
history = []   # LLM 의 "기억" — 매 호출마다 통째로 전송
while True:
    user = input("You: ")
    # 1. 사용자 발화 → history (role="user", parts=[{"text": ...}] 형식)
    history.append({"role": "user", "parts": [{"text": user}]})
    # 2. LLM 호출 — history 전체 전달해야 맥락 유지
    resp = client.models.generate_content(model=MODEL, contents=history)
    # 3. LLM 응답도 history 에 누적 (role="model")
    history.append({"role": "model", "parts": [{"text": resp.text}]})
    print("Model:", resp.text)
```

---

# Part 1 확장 실습

베이스라인 (`hello.py` + `chat.py`) 위에 본인 아이디어 추가

**확장 예시**
- 시스템 프롬프트 ("항상 영어로 답하라" 등)
- 대화 저장 / 불러오기
- 응답 스트리밍

**진행** — 기능 선택 → Copilot 구현 → 결과 공유

---

# Part 1 정리

LLM (머리) 사용 실습 완료

- `hello.py` — API 호출로 LLM 응답 받기
- `chat.py` — 멀티턴 챗봇 구현
- 확장 실습 — 본인 아이디어로 챗봇 커스터마이징

> Part 2 에서 도구 (팔다리) 를 달아 에이전트로

---

# Part 1 의 한계

- 대화만 가능. 외부 데이터 접근 불가
- LLM 이 파일 읽기 / 검색 / API 호출 등을 직접 수행 불가

**목표** — LLM 에 도구 (팔다리) 달기

> 도구 호출 패턴 → `tool_use.py`

---

<!-- _class: lead -->

# 🔧 Part 2 — 에이전트

`tool_use.py` → `agent_loop.py` → `agent_skill.py`

LLM 에 도구(팔다리) 를 달아 에이전트로 확장

---

# 머리(LLM)와 팔다리(도구)

<div class="body-diagram">
  <div class="head-box">LLM<br/><small>머리 — 사고</small></div>
  <div class="stem"></div>
  <div class="limbs-row">
    <div class="limb-box">read_note<br/><small>읽기</small></div>
    <div class="limb-box">list_notes<br/><small>목록</small></div>
    <div class="limb-box">search_notes<br/><small>검색</small></div>
  </div>
</div>

- LLM 단독 — 사고 가능, 외부 작업 불가
- 도구 = LLM 의 팔다리 (외부 세계와 상호작용)
- **에이전트 = 머리 + 팔다리**

---

# 도구 호출 — 4단계

1. **사용자 질문 + 도구 목록** → LLM 에 전달
2. **LLM** : "이 도구를 이렇게 부르세요" 요청 (텍스트 답변 X)
3. **우리 코드** 가 실제 함수 실행 → 결과 받음
4. **결과를 LLM 에 다시 전달** → LLM 이 자연어로 최종 답변

---

# Gemini SDK 의 주요 객체

| 객체 | 역할 |
|---|---|
| `genai.Client(api_key=)` | API 클라이언트 (Part 1) |
| `client.models.generate_content(...)` | LLM 호출 메서드 (Part 1) |
| `types.GenerateContentConfig` | 호출 옵션 (도구, 시스템 프롬프트) |
| `types.Tool` | 도구 선언 묶음 |

```python
from google.genai import types

config = types.GenerateContentConfig(tools=[...])
```

> SDK 가 제공하는 표준 형식. **import 해서 사용.**

---

# `GenerateContentConfig` 주요 옵션

| 옵션 | 역할 |
|---|---|
| `tools` | 도구 선언 (Part 2) |
| `system_instruction` | 시스템 프롬프트 (W2 에서 사용) |
| `temperature` | 응답 무작위성 (0~2, 낮을수록 일관) |
| `max_output_tokens` | 응답 최대 토큰 수 |
| `response_mime_type` | 응답 형식 (예: `"application/json"`) |

---

# `Tool` 주요 옵션

| 옵션 | 역할 |
|---|---|
| `function_declarations` | 우리 정의 함수 도구 (Part 2 에서 사용) |
| `google_search` | 구글 검색 (Gemini 내장) |
| `code_execution` | 코드 실행 (Gemini 내장) |

---

# LLM 마다 형식이 다름

개념은 같음 (function calling). **SDK 별로 키 이름 / 구조가 다름.**

| | Gemini | Claude | OpenAI |
|---|---|---|---|
| SDK | `google.genai` | `anthropic` | `openai` |
| 도구 호출 | `function_call` | `tool_use` | `tool_calls` |
| 도구 결과 | `function_response` | `tool_result` | `tool` role |
| Role | user / model | user / assistant | user / assistant / tool |

> Gemini 코드 그대로 Claude 못 씀

---

# 구현할 도구 — `read_note`

**목적** — `notes/` 폴더의 노트 파일 한 개 읽기

**시그니처**

```python
def read_note(filename: str) -> str
```

**예시 호출**

- `read_note("policy_leave.md")` → 휴가 정책 파일 내용
- `read_note("meeting_2026-05-19.md")` → 회의록 내용

> 이 도구를 LLM 에 등록 → LLM 이 알아서 호출

---

# `tool_use.py` — 도구 호출 한 턴

```python
# [1] 도구 함수 — 그냥 Python 함수 (LLM 은 직접 실행 못함)
def read_note(filename: str) -> str:
    return Path(NOTES_DIR / filename).read_text()

# [2] 도구 스키마 (declaration) 를 config 에 등록
config = types.GenerateContentConfig(tools=[types.Tool(function_declarations=[...])])

# [3] LLM 호출 → 응답에 function_call 이 들어있음 (텍스트 대신)
resp = client.models.generate_content(model=MODEL, contents=history, config=config)
fc = resp.candidates[0].content.parts[0].function_call
# fc.name = "read_note" / fc.args = {"filename": "policy_leave.md"}

# [4] ★ 우리가 함수 실행 + function_response 로 LLM 에 결과 돌려줌
result = read_note(**fc.args)
history.append({"role": "user", "parts": [{
    "function_response": {"name": fc.name, "response": {"result": result}}
}]})
```

---

# [2] 의 도구 선언 (`declaration`) 디테일

```python
read_note_declaration = {
    "name": "read_note",
    "description": "노트 파일 내용을 읽어 반환한다",
    "parameters": {
        "type": "object",
        "properties": {
            "filename": {
                "type": "string",
                "description": "예: policy_leave.md",
            },
        },
        "required": ["filename"],
    },
}
```

---

# `tool_use.py` 의 한계

- 한 턴만 도구 호출. 결과 보고 다시 호출 불가
- 복잡한 작업 (예: list → read 순서) 처리 불가

**목표** — 도구 호출의 반복 처리

> while 루프로 감싸기 → `agent_loop.py`

---

# 복잡한 작업을 처리하려면

**`tool_use.py` 의 한계**

- 도구 한 번 부르고 끝
- 여러 도구 조합해서 복잡한 작업 처리 불가

**해결** — LLM 이 결과 보고 **다음 도구 알아서 결정**

- 예: `list_notes` → `read_note` → 답변
- 도구 시퀀스를 LLM 이 자율 결정

→ `agent_loop.py` = LLM + 도구 + **결정 루프**

---

<!-- _class: lead -->

# 에이전트의 정의

# **LLM + 도구 + 반복 루프**

- 모든 에이전트의 공통 골격

---

# LLM 이 도구를 선택하는 법

사용자 질문 + `tool_declarations` 목록 → LLM → `function_call`

**LLM 의 판단 근거** — 각 도구의 `description`

| 사용자 질문 | LLM 의 선택 | 근거 (description) |
|---|---|---|
| "내 노트에 뭐 있어?" | `list_notes()` | "어떤 노트 파일들이 있는지" |
| "policy_leave.md 보여줘" | `read_note(...)` | "지정한 노트 파일 전체 내용" |
| "신입 연차 정책?" | `search_notes('연차')` | "파일명 모르고 키워드만 알 때" |

> `description` 이 LLM 의 도구 선택 기준
> 부정확하면 → LLM 이 잘못 부르거나 안 부름

---

# `agent_loop.py` — 도구 호출 반복

```python
TOOL_FUNCTIONS = {"list_notes": list_notes, "read_note": read_note}

for turn in range(MAX_TURNS):                # ★ 1. 반복 루프 (안전장치)
    resp = client.models.generate_content(...)
    function_calls = [...]                   # function_call 추출

    if not function_calls:                   # ★ 2. 종료 조건
        print(resp.text); break

    for fc in function_calls:
        result = TOOL_FUNCTIONS[fc.name](**fc.args)   # ★ 3. 도구 라우팅
        # function_response 형식으로 history 에 추가 (생략)
```

> 에이전트의 정체 = **반복 루프 / 종료 조건 / 도구 라우팅**

---

# 실행 흐름 — turn 별 추적

```
You: 가장 최근 회의록 한 줄로 요약해줘

--- turn 1 ---
[도구 요청] list_notes({})
[결과]      ['meeting_2026-05-12.md', 'meeting_2026-05-19.md', ...]

--- turn 2 ---
[도구 요청] read_note({'filename': 'meeting_2026-05-19.md'})
[결과]      # 5/19 주간 회의 ...

--- turn 3 ---
Model: 5월 19일 회의에선 인증 모듈 도입과 OJT 일정...
```

- LLM 이 list → read → 답변 순서로 도구 호출
- turn 3 에서 자연어 응답 → 루프 종료

---

# `agent_loop.py` 의 한계

질문 예시 — "신입사원 연차 정책 알려줘"

`list_notes` + `read_note` 만으로는:

- 파일명 모름 → `list_notes` 로 전체 목록 (~7개) 나열
- 어느 파일에 연차 정보? → 모든 파일 `read_note` → **토큰 낭비 / 비효율**

**해결** — 키워드 검색 도구 추가

- `search_notes("연차")` → 매칭 파일만 한 번에 반환

> 도구 함수 + 선언만 추가 → `agent_skill.py`

---

# `agent_skill.py` — 도구 추가

`agent_loop.py` + **도구 한 개 추가** (변경 두 곳)

```python
TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
    "search_notes": search_notes,    # ← 추가
}

tool_declarations = [
    {...}, {...},
    { "name": "search_notes", ... }  # ← 추가
]
```

agent loop 본문 (for + 종료 조건 + 라우팅) 은 **그대로**

---

# `agent_skill.py` — 동작 흐름

**질문 예시** — "신입사원인데 연차 언제부터 쓸 수 있어?"

LLM 의 처리 흐름:

1. 파일명 모르니 `search_notes("연차")` 로 매칭 파일 찾기
2. 결과 (`policy_leave.md` 등) → `read_note` 로 내용 읽기
3. 정책 내용 보고 자연어로 답변

---

# Part 2 확장 실습 — 새 도구 추가

`agent_loop.py` 에 새 도구 한 개 추가

**과제** — `get_current_time()` (현재 시간 반환, LLM 은 모름)

**진행 방식**
1. 함수 작성 (Copilot 활용 OK)
2. `agent_loop.py` 에 등록 (`TOOL_FUNCTIONS` + `tool_declarations`)
3. "지금 몇 시야?" 같은 질문으로 실행
4. 결과 공유

> 본인 도구 자유 시도 OK (예: `count_files`, `search_emails`)

---

# Part 2 정리

LLM 에 팔다리(도구) 달기 실습 완료

- `tool_use.py` — 도구 한 번 호출 (4단계 패턴)
- `agent_loop.py` — 반복 루프 = **에이전트**
- `agent_skill.py` — 도구 추가로 능력 확장
- 확장 실습 — 본인 도구로 커스터마이징

> 머리 (LLM) + 팔다리 (도구) + 반복 루프 = 에이전트

---

# 오늘 핵심 두 줄

1. **LLM API 호출** → 챗봇·에이전트 다 가능
2. **에이전트 = LLM + 도구 + 반복 루프**

