# Week 3 — RAG + 실전

이번 주 메시지는 단 하나:

> **에이전트 골격은 그대로. 도구만 search 가 추가될 뿐.**
>
> 그게 = **RAG**.

W2 의 에이전트는 `list_notes` + `read_note` 까지 했어요. 이번 주에 `search_notes` 추가 + `system_instruction` 으로 grounding = RAG 완성.

## 이번 주에 배우는 것

- **RAG** = Retrieval (검색 도구) + Augmented Generation (검색 결과 기반 답변)
- W2 agent_loop 위에 `search_notes` 만 추가 → 본질은 같음
- `system_instruction` 으로 LLM 답변 행동 제약 (할루시네이션 방지)
- 도구 3개 (`list`, `read`, `search`) 가 협업하는 실전 패턴

## 회차 끝나면 답할 수 있어야 하는 질문

1. RAG 가 왜 필요한가? W2 의 `list_notes` + `read_note` 만으론 부족한 이유는?
2. `agent_loop.py` 와 `rag.py` 의 차이를 코드로 짚을 수 있는가?
3. `system_instruction` 이 없으면 LLM 이 어떻게 답할까?
4. 본인 업무 도구를 이 골격에 어떻게 끼워넣을지 그려지는가?

---

## W2 → W3 의 진화

| | W2 | W3 |
|---|---|---|
| 도구 | `list_notes`, `read_note` | + `search_notes` |
| 시스템 프롬프트 | 없음 | "검색 결과에 근거해 답하라" |
| 사용자 질문 예 | "최근 회의록 한 줄 요약" | "신입사원 연차 정책 알려줘" |
| 동작 | list 한 다음 모든 read? 비효율 | search 한 번으로 관련 노트 찾기 |

→ search 한 줄이 "회사 위키 검색 에이전트" 의 핵심.

## 무엇을 만들 건가

**(1) RAG 의 본질** — `rag.py`. 도구 1개 (`search_notes`) + system_instruction
**(2) 실전 노트 도우미** — `notes_agent.py`. 도구 3개 (list + read + search) 통합

사용 예시 (`rag.py`):
```
You: 신입사원인데 연차 언제부터 쓸 수 있어?
[에이전트가 search_notes("연차 신입") 호출]
[검색 결과: policy_leave.md, onboarding.md 매칭]
에이전트: 신입사원은 입사 후 6개월 동안 월 1일씩 연차 부여받습니다. (출처: policy_leave.md)
```

## 어떻게 접근하나 — 바이브 코딩 사고법

### 단계별 사고

**1. 내가 뭘 만들 건가?**
LLM 이 모르는 정보 (내 노트) 를 **검색해서 그 내용에 근거해 답** 하는 에이전트.

**2. 어떤 구조?**
W2 의 agent_loop 골격 그대로. 도구만 `search_notes` 추가.
```
[W2 agent_loop]: tools = [list_notes, read_note]
[W3 rag.py]:     tools = [search_notes] + system_instruction
[W3 notes_agent.py]: tools = [list_notes, read_note, search_notes] + system_instruction
```

**3. 검색 결과를 LLM 한테 어떻게 줄까?**
W2 의 `function_response` 형식 그대로. 도구 결과 형식은 무엇이든 OK.

**4. LLM 이 검색 결과에 근거해 답하게 강제할 방법?**
`system_instruction` — "반드시 search 로 먼저 검색하고, 결과에 없는 내용은 추측 마라" 한 문장.

**5. 본인 업무에선?**
도구 함수 안의 구현만 바꿈 (사내 API, 슬랙 검색 등). 골격 동일.

---

## 직접 해야 하는 것

### (1) 손으로 짜보기 — `rag.py`

```bash
cd week3_rag
python rag.py
```

TODO 두 개:
- 검색 점수 계산 (`score = sum(...)`)
- `SYSTEM_INSTRUCTION` 작성 (할루시네이션 방지)

**생각해볼 거리**:
- 점수가 0 인 문서는 왜 제외?
- `SYSTEM_INSTRUCTION` 이 없으면 LLM 이 검색 안 하고 추측해서 답할 수도 있어요.

### (2) `agent_loop.py` ↔ `rag.py` 비교

두 파일 나란히 열고 diff 처럼 봐보세요. **다른 줄 몇 줄?**
- 도구 함수: `list_notes` / `read_note` → `search_notes`
- `system_instruction` 추가
- agent loop 30줄: **완전 동일**

→ "에이전트 골격은 그대로" 가 눈으로 들어옵니다.

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

LLM 이 알아서 적절한 도구를 고름.

### (5) Copilot 한테 시켜보기 — 본인 업무 도구

> "내 업무 도구를 agent loop 안에 끼워넣기"

본인 도구 시그니처 적고 Copilot 에:
```
이 함수 시그니처를 가진 도구를 만들고 agent loop 에 끼워줘.

def search_my_meeting_notes(keyword: str) -> list[dict]:
    """내 회의록 폴더에서 키워드 검색"""
    ...

- google.genai SDK
- system_instruction 으로 "검색 결과에만 근거해 답하라" 강제
- MAX_TURNS 안전장치
- 도구 본문은 mock 데이터로 (실제 파일 안 읽어도 됨)
```

받은 코드 평가: `rag.py` 와 구조 같은가?

---

## 회차 후 본인 적용

오늘 만든 본인 도구를 다음 주 (W4 LangChain) 에 그대로 가져옵니다.

> "내가 짠 이 골격 = LangChain 의 `create_react_agent` 한 줄."

준비: 본인 mock 도구 1개 (오늘 만든 거 그대로)

---

## 핵심 메시지 한 줄

> **agent loop 의 도구 자리에 무엇을 넣느냐가 에이전트의 정체.**
> 날씨 → 노트 검색 → 본인 업무. 골격은 그대로.
