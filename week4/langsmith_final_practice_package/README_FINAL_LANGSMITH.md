# LangSmith 수업 최종 실습 패키지

이 패키지는 수업 슬라이드의 LangSmith 파트를 모두 실습할 수 있도록 구성한 파일입니다.

## 실습 흐름

1. LangSmith 환경변수 설정
2. 최소 trace 테스트
3. RAG 동작 모니터링
4. 뉴스 요약 실행 및 prompt 개선용 trace 생성
5. Dataset / Annotation Queue 생성
6. LangSmith UI에서 score, correctness, note 피드백 입력
7. 피드백을 모아 개선 prompt 생성

---

## 0. 설치

```bash
conda activate mcp_class
pip install -r requirements.txt
```

환경 확인:

```bash
python 00_check_env.py
```

---

## 1. .env 만들기

Windows CMD:

```cmd
copy .env.example .env
```

PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

`.env` 파일을 열고 아래를 수정하세요.

```text
LANGSMITH_API_KEY=본인_LangSmith_API_Key
LANGSMITH_PROJECT=prompt_enhance_example
```

Ollama를 사용하는 경우:

```bash
ollama pull exaone3.5
ollama pull nomic-embed-text
```

Ollama가 없어도 일부 실습은 fallback 모드로 실행됩니다.

---

## 2. 최소 trace 테스트

```bash
python 01_minimal_trace.py
```

LangSmith 프로젝트에서 `classify_question`, `make_answer`, `minimal_demo_chain`이 보이는지 확인합니다.

---

## 3. RAG 동작 모니터링

```bash
python 02_rag_monitoring_ollama.py
```

질문 예시:

```text
전체 불량률은 얼마야?
냉매 누설 원인은 뭐야?
개선 조치는 뭐야?
exit
```

LangSmith에서 확인할 것:

- VectorStoreRetriever
- PromptTemplate
- ChatOllama
- StrOutputParser
- RunnableSequence input/output

---

## 4. 뉴스 요약 prompt 개선 trace 생성

```bash
python 03_news_summary_trace.py
```

LangSmith에서 `news_summary_chain` run을 확인합니다.

---

## 5. Dataset 및 Annotation Queue 생성

```bash
python 04_create_dataset_and_queue.py
```

LangSmith UI에서 다음을 확인합니다.

- Datasets → `prompt_enhance_example`
- Annotation Queues → `prompt_enhance_example_queue`

---

## 6. UI에서 피드백 입력

자세한 방법은 `06_UI_피드백_가이드.md`를 확인하세요.

평가 항목:

| 항목 | 유형 | 의미 |
|---|---|---|
| score | continuous | 0~5점 요약 품질 |
| correctness | categorical | correct / incorrect |
| notes | freeform | 자유 피드백 |

---

## 7. 피드백 기반 prompt 개선

UI에서 입력한 feedback을 직접 가져오기 어렵다면, 수업에서는 `sample_feedback.json`을 사용해도 됩니다.

```bash
python 05_combine_feedback_and_improve_prompt.py
```

이 파일은 여러 피드백을 run_id 기준으로 통합하고, 개선 prompt를 생성합니다.
