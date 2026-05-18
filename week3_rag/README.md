# Week 3 — RAG + 실전

이번 주의 메시지는 단 하나:

> **에이전트 골격은 그대로. 도구만 바뀐다.**
>
> `rag.py` 의 핵심 코드를 2주차 `agent_loop.py` 와 비교해보면 거의 똑같습니다.
> 다른 것은 ① 도구 함수 (`get_weather` → `search_docs`),
> ② `system_instruction` 추가 — 둘뿐.

## 학습 목표

- **RAG = Retrieval(도구로 정보 찾기) + Augmented Generation(찾은 내용에만 근거해 답하기)**
- 검색 도구를 통해 LLM 의 할루시네이션을 줄이는 패턴
- 하드코딩 문서 → 진짜 파일 시스템으로 자연스럽게 확장 (`notes_agent.py`)

## 파일과 실행 순서

| # | 파일 | 무엇을 배우나 |
|---|---|---|
| 1 | `rag.py` | 가짜 사내 위키 (`DOCS` 리스트) 를 검색하는 RAG 에이전트 |
| 2 | `notes_agent.py` | 실제 디스크의 파일을 검색·읽는 실전 데모 (도구 3개) |

```bash
python rag.py

# notes_agent.py 는 기본적으로 현재 폴더를 검색합니다
python notes_agent.py

# 본인 노트 폴더를 검색하려면 (예시 경로 — 본인 경로로 바꿔주세요)
NOTES_DIR=C:/Users/이름/Dropbox/notes python notes_agent.py   # Windows
NOTES_DIR=/Users/이름/Dropbox/notes python3 notes_agent.py    # macOS
```

## 핵심 비교: agent_loop.py ↔ rag.py

같은 골격 위에 도구만 바꾼 것을 직접 눈으로 확인하세요.

```
agent_loop.py:  tools = [get_weather, recommend_outfit]
rag.py:         tools = [search_docs] + system_instruction
notes_agent.py: tools = [list_files, read_file, search_files] + system_instruction
```

→ **다음 단계 (B반 후반)**: 이 패턴 그대로, `tools` 자리에 본인 업무 도구만 넣으면 자기만의 에이전트가 만들어집니다.

## 끝나면 생각해볼 거리 (B반 후반 발표용)

- 2주차에서 식별한 본인 업무 도구 (사내 위키 검색, 폴더 정리, JIRA 조회 등)
  중 **하나** 를 골라 Python 함수 + tool_declaration 로 작성해보기
- `notes_agent.py` 의 `TOOL_FUNCTIONS` / `tool_declarations` 만 갈아끼우면 완성
