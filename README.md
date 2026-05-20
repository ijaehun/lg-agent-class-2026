# LG KAMP · AI 에이전트 강의 (2026)

LG KAMP 3주 AI 에이전트 강의의 실습 코드 + 자료 저장소.
"에이전트의 정체를 코드 한 줄씩 직접 짜서 분해해보는" 것이 목표입니다.

## 어디서 시작하나요?

1. **`SETUP.md`** — Python 설치부터 Gemini API 키 설정까지 사전 준비
2. **`week0_setup/README.md`** — Week 0 (환경 점검 + Copilot 첫 실습) 안내
3. 그 뒤로 `week1_llm_agent/` → `week2_rag_langchain/` → `week3_mcp/` 순서로 진행

## 폴더 구조

```
notes/                  모든 회차가 공유하는 샘플 노트 (정책, 회의록, 온보딩)
week0_setup/            Week 0: 환경 점검 + Copilot 실습
week1_llm_agent/        Week 1: LLM + 에이전트 + RAG 맛 (Part 1 + Part 2)
week2_rag_langchain/    Week 2: RAG 심화 + LangChain 한 줄로
week3_mcp/              Week 3: MCP 표준 + 종강
solutions/              강사용 완성본 (혼자 풀어보고 확인할 때만 열어보세요)
```

## 강의 흐름 — 3주에 걸쳐 "내 노트 검색 도우미" 점진적 완성

매주 같은 에이전트가 더 똑똑해져요. `notes/` 폴더의 사내 문서가 공유 데이터.

| 주차 | 주제 | 핵심 파일 | 에이전트의 능력 |
|---|---|---|---|
| 0 | 환경 + Copilot 실습 | `copilot_play.py` | (셋업) |
| **1** | **LLM + 에이전트 + RAG 맛** | `hello.py` `chat.py` `tool_use.py` `agent_loop.py` `agent_skill.py` | LLM 호출 → 도구로 노트 읽기 → 검색 도구 추가 = **RAG 의 본질** |
| **2** | **RAG 심화 + LangChain** | `rag.py` `notes_agent.py` `langchain_agent.py` | `system_instruction` grounding + 같은 일을 **LangChain 한 줄로** |
| **3** | **MCP 표준 + 종강** | `mcp_server.py` | 도구를 **표준 단자로** 노출 (Claude Desktop 에서 직접 사용) |

## 학습 방식

- 각 `week*/` 폴더의 `.py` 파일에 **`# TODO`** 와 **`___`** 빈칸이 있어요.
- 강의 시간에 같이 채워나가요. 왜 이렇게 짜야 하는지 함께 짚어볼 거예요.
- 마지막 회차에는 이 골격 위에서 본인 업무 도구로 변형해보는 데까지 갑니다.

## 강의 끝난 뒤 다시 와도 돼요

각 `weekN_*/README.md` 만 봐도 흐름을 다시 따라갈 수 있게 짰어요.
혼자 풀다가 막히면 강의 단체방에 편하게 물어봐주세요.
