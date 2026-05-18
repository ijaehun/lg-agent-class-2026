# Week 2 — 에이전트의 정체

W1 에서 발견한 한계 — "LLM 이 내 노트를 모름" — 을 **도구로** 해결합니다.
이번 주가 강의 전체에서 가장 중요한 회차예요.

## 이번 주에 배우는 것

- LLM 응답이 **텍스트 대신 function_call** 일 수 있다는 것
- 그 요청을 받아 **우리 코드가 함수 실행 후 결과를 돌려주는** 패턴 (도구 호출 4단계)
- `while` 로 감싸면 = **에이전트**
- W1 의 에이전트 (= 그냥 LLM 호출) → W2 에서 도구로 **노트를 읽을 수 있게** 됨

## 회차 끝나면 답할 수 있어야 하는 질문

1. LLM 이 "함수를 호출했다" 는 게 무슨 뜻인가?
2. 도구가 없으면 LLM 이 못 하는 일은 무엇? (W1 에서 본 그 한계)
3. `while` 루프가 왜 필요한가?
4. **Copilot 이 짜준 agent loop 코드를 보고 옳은지 평가할 수 있는가?**

→ 이 네 가지가 본인 입에서 자연스럽게 나오면 성공.

---

## 무엇을 만들 건가

**노트를 읽을 수 있는 에이전트**.

`tool_use.py` — 한 턴만 (도구 1개: `read_note`)
`agent_loop.py` — 루프 (도구 2개: `list_notes` + `read_note`)

사용 예시 (`agent_loop.py`):
```
You: 내 노트에 무슨 회의록이 있어? 가장 최근 회의록 한 줄로 요약해줘
↓
[에이전트가 알아서 도구 두 번 호출]
  1. list_notes() → ["meeting_2026-05-12.md", "meeting_2026-05-19.md", "onboarding.md", ...]
  2. read_note("meeting_2026-05-19.md") → 회의록 전문
↓
에이전트: 5월 19일 회의에선 인증 모듈 외부 라이브러리 도입과 신입 OJT 일정을 다뤘어요.
```

→ W1 에선 LLM 이 "회의록을 모릅니다" 했는데, W2 에선 **읽고 답함**.

## 어떻게 접근하나 — 바이브 코딩 사고법

### 단계별 사고

**1. 내가 뭘 만들 건가?**
사용자 질문 → 시스템이 알아서 노트 읽고 답.

**2. 어떤 구조?**
LLM 혼자선 노트 못 읽음. 그래서 우리 Python 코드가 노트 읽어주는 **도구** 필요.
```
사용자 → LLM → (도구 호출 요청) → 우리 코드 (read_note) → 결과 → LLM → 사용자
```

**3. 한 번에 끝나나?**
"가장 최근 회의록 요약" 같은 질문엔 도구 두 번 (list → read) 필요. → **반복 (while)**.

**4. 언제 멈추나?**
LLM 이 도구 안 부르고 **자연어 텍스트로 답할 때** = 끝.

**5. 안전장치는?**
LLM 이 무한히 도구만 부르면? → `MAX_TURNS` 상한.

→ 이 다섯 단계가 머리에 있으면 코드 직접 짜든 Copilot 시키든 같은 결과.

---

## 직접 해야 하는 것

### (1) 손으로 짜보기 — `tool_use.py`

도구 호출 **한 턴** 의 4단계 흐름 손에 익히기.

```bash
cd week2_agent
python tool_use.py
```

기본 질문: `"policy_leave.md 파일 내용을 한 줄로 요약해줘"` — LLM 이 `read_note("policy_leave.md")` 호출 → 결과 받고 답.

TODO 두 개:
- `read_note(**function_call.args)` — 도구 실제 실행
- `function_response` 형식의 dict — LLM 에 결과 돌려주기

**생각해볼 거리**:
- `**` 두 개의 의미는?
- `function_response` 의 role 이 왜 `"user"` 일까?

### (2) 망가뜨려보기 — "왜 이렇게 짜야 하는지" 직접 보기

| 망가뜨릴 곳 | 예상 결과 |
|---|---|
| `function_response` 의 dict 를 평범한 텍스트로 | LLM 이 결과를 못 알아듣고 다시 호출 시도 |
| `read_note_declaration` 의 description 빈 문자열 | LLM 이 도구를 안 부르거나 잘못 부름 |
| `read_note` 함수가 `return ""` 하도록 | LLM 이 "내용을 알 수 없습니다" 라고 답 |

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

### (4) Copilot 한테 시켜보기 — 같은 에이전트

빈 파일 `my_agent.py` 만들고 Copilot 에:

**좋은 프롬프트**:
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

### (5) Copilot 답 평가하기 — 체크리스트

- [ ] `while` 루프 있는가? 종료 조건은?
- [ ] `function_call` 이 없을 때 어떻게 처리?
- [ ] `function_response` 형식이 우리 코드와 같은가?
- [ ] `MAX_TURNS` 안전장치 있는가?
- [ ] 도구 두 번 호출되는 시나리오가 잘 동작?

차이가 있다면 우리 솔루션과 비교 — **어느 게 더 나은가? 왜?**

---

## 회차 후 본인 적용 (다음 주 준비)

지금 에이전트는 **파일명을 알아야** 읽을 수 있어요.
"신입사원 연차 정책이 뭐야?" 같은 질문엔 어떻게 답할까?
→ list_notes 로 파일 다 가져온 다음 하나씩 read_note? 비효율적이고 토큰 낭비.

**다음 주 (W3) = 키워드로 검색하는 도구 추가** → 그러면 우리는 RAG 를 만든 셈.

머릿속에 한 줄로:
> "내 업무에서 '검색 → 읽기 → 답변' 형태로 자동화하고 싶은 게 무엇?"

---

## 핵심 메시지 한 줄

> **에이전트 = LLM + 도구 + 반복 루프. 그게 전부.**
> 오늘 한 번 손으로 짠 이유 — 다음 주부터 Copilot 시켜도 답이 옳은지 평가할 수 있게.
