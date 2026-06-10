# 로컬 LLM 기반 MCP 실습 전체 파일

이 폴더는 수업 슬라이드에 나온 예제를 모두 따라갈 수 있도록 만든 실습 코드입니다.

## 실습 예제

1. **MCP 예제1: 기본 Tool 호출**
   - add
   - 현재 폴더 조회
   - 스크린샷 캡처

2. **MCP 예제2: 문서 Q&A MCP 서버**
   - 문서 업로드
   - 문서 임베딩
   - 로컬 벡터 DB 저장
   - 질문응답

3. **MCP 예제3: 날씨 정보 조회 API**
   - WeatherAPI 연결
   - 날씨 Tool 생성
   - 날씨 질문 판별
   - 한국어/영어 처리
   - 번역 함수 구조

---

## 0. 가장 먼저 할 일

### 0-1. 압축 해제 후 폴더 이동

```bash
cd mcp_class_all_examples
```

### 0-2. 가상환경 생성

```bash
conda create -n mcp_class python=3.11 -y
conda activate mcp_class
```

### 0-3. 라이브러리 설치

```bash
pip install -r requirements.txt
```

설치 확인:

```bash
python 00_check_environment.py
```

---

## 1. MCP 예제1: 기본 Tool 호출

### 1-1. 서버 실행

터미널 1:

```bash
python example1_basic_tools/server_basic_tools.py
```

### 1-2. 클라이언트 실행

터미널 2:

```bash
python example1_basic_tools/client_basic_tools.py
```

확인할 것:

- 서버에 등록된 Tool 목록이 출력되는가?
- add Tool 결과가 나오는가?
- 현재 폴더 정보가 나오는가?
- 스크린샷 Tool이 성공 또는 실패 메시지를 반환하는가?

---

## 2. MCP 예제2: 문서 Q&A MCP 서버

이 코드는 Ollama가 없어도 실행됩니다.  
Ollama가 있으면 로컬 LLM 답변을 생성하고, 없으면 간단한 검색 기반 답변으로 대체됩니다.

### 2-1. 선택 사항: Ollama 준비

```bash
ollama pull exaone3.5
```

### 2-2. 문서 Q&A 서버 실행

터미널 1:

```bash
python example2_document_qa/server_document_qa.py
```

### 2-3. 문서 Q&A 클라이언트 실행

터미널 2:

```bash
python example2_document_qa/client_document_qa.py
```

확인할 것:

- `sample_quality_report.txt`가 업로드되는가?
- 문서 chunk가 몇 개 생성되는가?
- "불량률", "원인", "개선 조치" 질문에 답변하는가?

---

## 3. MCP 예제3: 날씨 API MCP Tool

WeatherAPI Key가 없어도 샘플 날씨 데이터로 실행됩니다.  
Key가 있으면 실제 WeatherAPI를 호출합니다.

### 3-1. 선택 사항: WeatherAPI Key 설정

```bash
copy .env.example .env
```

Windows가 아니면:

```bash
cp .env.example .env
```

`.env` 파일을 열고 아래 값을 수정합니다.

```text
WEATHER_API_KEY=본인_API_KEY
```

### 3-2. 날씨 서버 실행

터미널 1:

```bash
python example3_weather_api/server_weather.py
```

### 3-3. 날씨 챗봇 클라이언트 실행

터미널 2:

```bash
python example3_weather_api/client_weather_chatbot.py
```

테스트 질문:

```text
서울 날씨 알려줘
오늘 창원 우산 가져가야 하나요?
What's the weather in London?
1+1은 뭐야?
exit
```

---

## 학생들이 어려워할 때

먼저 아래 파일로 MCP 없이 함수 호출 구조만 보여주세요.

```bash
python warmup_no_mcp.py
```

이후 MCP 예제로 넘어가면 이해가 훨씬 쉽습니다.
