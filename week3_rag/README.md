# Week 3 — RAG + 실전

이번 주 메시지는 단 하나:

> **에이전트 골격은 그대로. 도구만 바뀐다.**

`agent_loop.py` (W2) 의 도구 자리에 **검색 도구** 가 들어가면 = RAG.
하드코딩 문서를 **실제 파일 시스템** 으로 바꾸면 = 실전 검색 에이전트.

## 이번 주에 배우는 것

- **RAG** = Retrieval (도구로 정보 찾기) + Augmented Generation (찾은 내용에만 근거해 답하기)
- agent_loop 골격 위에 `search_docs` 도구를 얹는 패턴
- `system_instruction` 으로 LLM 의 답변 행동을 제약 (할루시네이션 방지)
- 진짜 파일 시스템 검색 — 도구 3개 (`list`, `read`, `search`) 가 협업

## 회차 끝나면 답할 수 있어야 하는 질문

1. RAG 가 왜 필요한가? LLM 만으로 안 되는 일은 무엇?
2. `agent_loop.py` 와 `rag.py` 의 차이를 코드로 짚을 수 있는가?
3. `system_instruction` 이 없으면 LLM 이 어떻게 답할까?
4. 검색 결과에 없는 질문을 받으면 LLM 이 뭐라고 답해야 옳은가? (그리고 어떻게 그렇게 만드나?)
5. 내 업무 도구를 이 골격에 어떻게 끼워넣을지 그려지는가?

---

## 무엇을 만들 건가

**(1) 사내 위키 검색 에이전트** (`rag.py`) — 하드코딩 문서 4개에서 키워드로 검색
**(2) 내 노트 검색 에이전트** (`notes_agent.py`) — 실제 디스크의 파일을 list/read/search

사용 예시 (`rag.py`):
```
You: 신입사원인데 연차 언제부터 쓸 수 있어?
[에이전트가 search_docs("연차 신입") 호출]
[검색 결과로 "연차 사용 정책" 문서 받음]
에이전트: 신입사원은 입사 후 6개월 동안 월 1일씩 부여받습니다. (출처: 연차 사용 정책)
```

## 어떻게 접근하나 — 바이브 코딩 사고법

### 단계별 사고

**1. 내가 뭘 만들 건가?**
LLM 이 모르는 정보 (사내 문서) 를 **검색해서 그 내용에 근거해 답** 하는 에이전트.

**2. 어떤 구조?**
W2 에서 짠 agent loop 가 골격. 도구 자리에 `search_docs` 만 넣으면 됨.
```
[W2 agent_loop]: tools = [get_weather, recommend_outfit]
[W3 rag.py]:     tools = [search_docs]
```
**골격 코드는 거의 그대로** (한 줄씩 짚어볼 거예요).

**3. 도구 결과를 LLM 한테 어떻게 줄까?**
W2 에서 본 `function_response` 형식 그대로. 도구 결과는 형식만 맞으면 무엇이든 OK.

**4. LLM 이 검색 결과에 근거해 답하게 강제할 방법?**
`system_instruction` — "반드시 search_docs 로 먼저 검색하고, 결과에 없는 내용은 추측하지 마라" 한 문장.

**5. 진짜 파일 시스템에선?**
도구를 1개 → 3개로 (`list_files`, `read_file`, `search_files`). 골격은 동일. **이게 본인 업무용 에이전트의 baseline 입니다.**

→ "도구만 갈아끼우면 어떤 정보 시스템이든 RAG 가능" 이라는 패턴 체득.

---

## 직접 해야 하는 것

### (1) 손으로 짜보기 — `rag.py`

```bash
cd week3_rag
python rag.py
```

TODO 두 개:
- 검색 점수 계산 (`score = sum(...)`)
- `SYSTEM_INSTRUCTION` 작성 (할루시네이션 방지 프롬프트)

**생각해볼 거리**:
- 검색 점수가 0 인 문서는 왜 제외할까?
- `SYSTEM_INSTRUCTION` 이 없으면 LLM 이 검색 안 하고 추측해서 답할 수도 있어요. 그걸 어떻게 막을지?

### (2) `agent_loop.py` ↔ `rag.py` 비교

두 파일을 나란히 열고 diff 처럼 봐보세요. **다른 줄이 몇 줄?**
- 도구 함수: `get_weather` → `search_docs`
- 도구 스키마: 이름·설명만 다름
- `system_instruction` 추가
- agent loop 30줄: **완전 동일**

→ "에이전트 골격은 그대로" 라는 메시지가 눈으로 들어옵니다.

### (3) 망가뜨려보기

| 망가뜨릴 곳 | 무슨 일이 일어나는지 예상 |
|---|---|
| `SYSTEM_INSTRUCTION` 을 빈 문자열로 | LLM 이 검색 안 하고 추측해서 답할 수 있음 |
| `search_docs` 의 description 을 빈 문자열로 | LLM 이 도구를 안 부름 |
| `search_docs` 가 빈 리스트만 반환하도록 | LLM 이 "문서에 없습니다" 라고 답해야 옳음 — 실제로 그렇게 답하는지 확인 |

### (4) 실전 — `notes_agent.py`

진짜 파일 검색. 본인 노트 폴더를 가리키게 환경변수 설정:

```powershell
# Windows
$env:NOTES_DIR="C:\본인\문서폴더"; python notes_agent.py

# macOS
NOTES_DIR=/Users/본인/문서폴더 python3 notes_agent.py
```

TODO 1 개:
- `TOOL_FUNCTIONS` 딕셔너리 (도구 이름 → 함수 매핑)

**자기 노트에서 실제 답을 받아보세요.** 이게 본인 업무용 에이전트의 시작점입니다.

### (5) Copilot 한테 시켜보기 — 본인 업무 도구

> "내 업무 도구 1개를 agent loop 안에 넣어보기"

W2 끝에 생각해둔 본인 도구 (회의록 검색 / 사내 위키 조회 / 이메일 필터 등) 를 시그니처로 적고 Copilot 에 시키기:

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

받은 코드 평가 — `rag.py` 와 구조 같은가? 다른 점이 있다면 왜?

---

## 회차 후 본인 적용

이번 주에 본인 도구 1개를 만들어봤다면 — **다음 주 (LangChain) 가 핵심**.

> "내가 짠 이 골격이 LangChain 의 `create_react_agent` 한 줄과 동등하다는 걸 직접 본다."

다음 주를 위한 준비:
- 본인 mock 도구 1개 (오늘 만든 거 그대로 가져오기)

---

## 핵심 메시지 한 줄

> **agent loop 의 도구 자리에 무엇을 넣느냐가 에이전트의 정체.**
> 날씨 → RAG → 본인 업무. 골격은 그대로. 본인이 짠 도구로 갈아끼우는 순간, 그게 본인의 에이전트.
