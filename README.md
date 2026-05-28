# LG KAMP · AI 에이전트 강의자료 (2026)

LG KAMP AI 에이전트 강의자료 — Jupyter notebook + Marp 슬라이드.

## 어디서 시작하나요?

1. **`SETUP.md`** — Python 설치부터 Gemini API 키 설정까지 사전 준비
2. `week1_llm_agent/` (Week 1) → `week2/week2.ipynb` (Week 2) 순서로 진행

## 폴더 구조

```
notes/              공유 데이터 예시 (정책, 회의록, 온보딩)
week1_llm_agent/    Week 1: LLM + 에이전트 (.py 파일)
week2/              Week 2: RAG + LangChain + MCP (Jupyter notebook)
  ├── week2.ipynb     메인 자료 — cell 한 개씩 실행하며 진행
  └── mcp_server.py   MCP 서버 예시 (Part 3 에서 코드 확인용)
lessons/            강의 슬라이드 (Marp)
  ├── week1_slides.md
  └── week2_slides.md
```

## 강의 흐름 — "내 노트 검색 도우미" 점진적 완성

`notes/` 폴더의 **사내 문서 예시** 가 공유 데이터. 같은 에이전트가 더 똑똑해짐.

| 회차 | 주제 | 메인 자료 | 에이전트의 능력 |
|---|---|---|---|
| W1 | LLM + 에이전트 | `week1_llm_agent/*.py` | LLM 호출 → 도구로 노트 읽기 → 검색 도구 추가 |
| W2 | RAG + LangChain + MCP | `week2/week2.ipynb` | `system_instruction` grounding + LangChain 한 줄로 + MCP 표준 도구화 |

## 학습 방식

**W2** = Jupyter notebook 으로 **cell 한 개씩 같이 실행** 하며 진행. 슬라이드 (`lessons/`) 는 개념 / 섹션 전환용.

## 강의 끝난 뒤 다시 와도 돼요

이 README + 슬라이드 + notebook 보면서 다시 따라갈 수 있어요.
혼자 풀다가 막히면 강의 단체방에 편하게 물어봐주세요.
