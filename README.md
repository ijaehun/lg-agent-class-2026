# LG LLM 에이전트 강의 (2026)

LG 연구원 대상 4주 LLM 에이전트 강의의 실습 코드 + 자료 저장소.
"에이전트의 정체를 코드 한 줄씩 직접 짜서 분해해보는" 것이 목표입니다.

## 어디서 시작하나요?

1. **`SETUP.md`** — Python 설치부터 Gemini API 키 설정까지 사전 준비
2. **`week0_setup/README.md`** — Week 0 (환경 점검 + Copilot 첫 체험) 안내
3. 그 뒤로 `week1_llm/` → `week2_agent/` → `week3_rag/` → `week4_mcp/` 순서로 진행

## 폴더 구조

```
week0_setup/     Week 0: 환경 점검 + Copilot 체험
week1_llm/       Week 1: LLM 호출의 가장 작은 단위 (hello, chat)
week2_agent/     Week 2: 에이전트 정체 (tool_use, agent_loop)
week3_rag/       Week 3: RAG + 실전 (rag, notes_agent)
week4_mcp/       Week 4: MCP 표준 (mcp_server + Claude Desktop)
solutions/       강사용 완성본 (스스로 풀고 확인할 때만 열어보세요)
lessons/         강사용 분단위 시나리오
```

## 강의 흐름

| 주차 | 주제 | 핵심 파일 |
|---|---|---|
| 0 | 환경 + Copilot 체험 | `week0_setup/copilot_play.py` |
| 1 | LLM 다루기 | `hello.py` + `chat.py` |
| 2 | 에이전트 정체 | `tool_use.py` + `agent_loop.py` |
| 3 | RAG + 실전 | `rag.py` + `notes_agent.py` |
| 4 | MCP 표준 + 종강 | `mcp_server.py` + Claude Desktop |

## 학습 방식

- 각 `week*/` 폴더의 `.py` 파일에 **`# TODO`** 와 **`___`** 빈칸이 있어요.
- 강의 시간에 같이 채워나가요. 왜 이렇게 짜야 하는지 함께 짚어볼 거예요.
- 마지막 회차에는 이 골격 위에서 본인 업무 도구로 변형해보는 데까지 갑니다.

## 강의 끝난 뒤 다시 와도 돼요

각 `weekN_*/README.md` 만 봐도 흐름을 다시 따라갈 수 있게 짰어요.
혼자 풀다가 막히면 강의 단체방에 편하게 물어봐주세요.
