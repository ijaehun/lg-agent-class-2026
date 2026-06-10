# LG KAMP · AI 에이전트 강의자료 (2026)

LG전자–국립창원대 KAMP AI 에이전트 강의자료 모음.
실습 코드(Python / Jupyter) + 슬라이드 + 강의 PDF.

## 시작하기

1. **`SETUP.md`** — Python 설치부터 Gemini API 키 설정까지 사전 준비
2. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

## 폴더 구조

```
week1/        LLM + 에이전트 기초 (.py + 슬라이드 + 공유 데이터 notes/)
week2/        RAG + LangChain + MCP (Jupyter notebook + 슬라이드)
week3/        (실습 공간)
week4/        RAG 심화 + MCP 실습 모음 + 강의 PDF
```

각 주차 폴더 안에 코드 · 슬라이드 · 데이터가 함께 들어 있습니다.

## 회차별 자료

| 회차 | 주제 | 메인 자료 |
|---|---|---|
| Week 1 | LLM + 에이전트 기초 | `week1/*.py` · `week1/week1_slides.md` |
| Week 2 | RAG + LangChain + MCP | `week2/week2.ipynb` · `week2/week2_slides.md` |
| Week 4 | RAG 심화 + MCP 실습 | `week4/` (아래 참고) · 강의 PDF (KAMP 5·6일차) |

## week4 실습 목록

| 폴더 | 내용 |
|---|---|
| `pdf_rag_practice/` | PDF 문서 기반 RAG (터미널) |
| `advanced_rag_practice/` | PDF 기반 RAG 심화 |
| `chatbot_rag_practice/` | 여러 PDF 업로드 + 웹 챗봇 RAG |
| `multimodal_rag_practice/` | 이미지 기반 멀티모달 RAG |
| `web_crawling_practice/` | 웹 페이지 크롤링 기반 RAG |
| `mcp_class_all_examples/` | MCP 실습 (기본 Tool / 문서 Q&A / 날씨 API) |

각 실습 폴더의 `.md` 파일에 실행 방법과 설명이 들어 있습니다.
MCP 실습은 `week4/mcp_class_all_examples/.../README_수업순서.md` 참고.

## 환경

- Python `venv` + `pip` + Jupyter
- 모델: Gemini 2.5 Flash (`google-genai` SDK)
- API 키 설정은 `SETUP.md` 참고
