# LG KAMP · AI 에이전트 강의자료 (2026)

LG KAMP 3주 AI 에이전트 강의자료 — 베이스라인 코드 + Marp 슬라이드.

## 어디서 시작하나요?

1. **`SETUP.md`** — Python 설치부터 Gemini API 키 설정까지 사전 준비
2. `week1_llm_agent/` → `week2_rag_langchain/` → `week3_mcp/` 순서로 진행

## 폴더 구조

```
notes/                  공유 데이터 예시 (정책, 회의록, 온보딩)
week1_llm_agent/        Week 1: LLM + 에이전트
week2_rag_langchain/    Week 2: RAG 심화 + LangChain
week3_mcp/              Week 3: MCP 표준 + 종강
lessons/                강의 슬라이드 (Marp)
```

> 각 `weekN_*/` 폴더 = **베이스라인 완성 코드**. 슬라이드 (`lessons/`) 와 함께 학습.

## 강의 흐름 — 3주에 걸쳐 "내 노트 검색 도우미" 점진적 완성

매주 같은 에이전트가 더 똑똑해져요. `notes/` 폴더의 **사내 문서 예시** 가 공유 데이터.

| 주차 | 주제 | 핵심 파일 | 에이전트의 능력 |
|---|---|---|---|
| **1** | **LLM + 에이전트** | `hello.py` `chat.py` `tool_use.py` `agent_loop.py` `agent_skill.py` | LLM 호출 → 도구로 노트 읽기 → 검색 도구 추가 |
| **2** | **RAG 심화 + LangChain** | `rag.py` `notes_agent.py` `langchain_agent.py` | `system_instruction` grounding + 같은 일을 **LangChain 한 줄로** |
| **3** | **MCP 표준 + 종강** | `mcp_server.py` | 도구를 **표준 단자로** 노출 (Claude Desktop 에서 직접 사용) |

## 학습 방식

- 각 `weekN_*/` 폴더 = **베이스라인 완성 코드** (바로 실행 가능)
- 슬라이드 (`lessons/`) 보면서 코드 구조 파악
- **Copilot 으로 같은 / 확장 코드 짜보며 비교** — 본인 업무에 맞게 응용
- 결과는 **[Live Code Share](http://3.38.129.150/)** 에 제출 → 발표뷰에서 다같이 비교

## 강의 끝난 뒤 다시 와도 돼요

이 README + 슬라이드 (`lessons/`) 보면서 다시 따라갈 수 있어요.
혼자 풀다가 막히면 강의 단체방에 편하게 물어봐주세요.
