# 로컬 RAG + Role-Based Multi-Agent 실습

## 1. 실습 목표

이 실습은 MCP 없이 RAG와 Tool Registry를 기반으로 multi-agent workflow의 전체 구조를 먼저 확인하기 위한 예제입니다.
코딩 경험이 적은 수강생은 완성본을 먼저 실행해 보고, 이후 Copilot/ChatGPT를 이용해 같은 구조를 바이브코딩으로 다시 구현합니다.

## 2. 프로젝트 구조

```text
multi_agent_rag_lab/
  config.py
  llm.py
  rag.py
  tools.py
  prompts.py
  agent.py
  multi_agent.py
  chat_cli.py
  build_index.py
  data/
    reference/
      *.txt
    logs/
      test_log_sample.csv
  vector_store/
  outputs/
```

## 3. 사전 준비

```bash
pip install -r requirements.txt
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

Ollama 없이 구조만 먼저 확인하려면 `config.py`에서 다음 값으로 변경합니다.

```python
USE_MOCK_LLM = True
```

## 4. RAG index 생성

```bash
python build_index.py
```

## 5. 실행

```bash
python chat_cli.py
```

추천 입력:

```text
도어 결로 VOC와 시험 로그를 참고해서 원인 후보, 추가 확인 항목, 고객 대응 초안을 정리해줘.
```

## 6. 수업에서 설명할 핵심

- RAG는 외부 문서를 검색해서 근거 context를 만드는 구조이다.
- Tool은 LLM이 직접 하기 어려운 검색, 계산, 저장을 담당한다.
- Single Agent는 하나의 controller가 tool 선택과 응답 생성을 처리한다.
- Multi-Agent는 검색, 분석, 작성, 검토 역할을 분리한다.
- 이번 실습은 자유 대화형 multi-agent가 아니라 role-based workflow이다.


## 콘솔 로그 확인

이번 버전은 수강생이 실행 흐름을 눈으로 따라갈 수 있도록 단계 로그를 출력합니다.

예시는 다음과 같습니다.

```text
[14:20:01] ▶ Multi-Agent Workflow 시작
[14:20:01] ▶ Multi-Agent 1/4: Search Agent 실행
[14:20:02] ▶ Tool 실행 - search_manual
[14:20:02] ▶ RAG 검색 시작 - query=도어 결로 VOC와 시험 로그를 참고해서...
    → 검색 모드: vector
    → 검색 결과 수: 3
[14:20:05] ▶ Multi-Agent 2/4: Analysis Agent 실행
[14:20:05] ▶ Tool 실행 - analyze_test_log
[14:20:08] ▶ Multi-Agent 3/4: Writer Agent 실행
[14:20:11] ▶ Multi-Agent 4/4: Reviewer Agent 실행
[14:20:13] ▶ Tool 실행 - save_report
[14:20:13] ▶ Multi-Agent Workflow 완료
```

로그 출력은 `logger.py`에서 관리합니다. 핵심 기능은 유지하고, `log_step()`, `log_detail()`, `log_result()`로 현재 실행 단계를 보여주는 방식입니다.
