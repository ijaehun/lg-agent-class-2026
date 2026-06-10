import os
from pathlib import Path
import requests
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "exaone3.5")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_GENERATE_URL = f"{OLLAMA_BASE_URL}/api/generate"
ARTICLE_PATH = Path("sample_news_article.txt")

@traceable(name="load_news_article")
def load_news_article() -> str:
    return ARTICLE_PATH.read_text(encoding="utf-8")

@traceable(name="make_prompt")
def make_prompt(article: str, instruction: str, feedback: str = "") -> str:
    return f'''
당신은 제조 AI 교육용 뉴스 요약 도우미입니다.

[요약 지시사항]
{instruction}

[이전 피드백]
{feedback if feedback else "아직 피드백 없음"}

[뉴스 원문]
{article}

[요약]
'''.strip()

def ollama_available() -> bool:
    try:
        return requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=2).status_code == 200
    except Exception:
        return False

@traceable(name="summary_llm_or_fallback")
def summarize(prompt: str, article: str) -> str:
    if ollama_available():
        response = requests.post(
            OLLAMA_GENERATE_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=120,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    sentences = [s.strip() for s in article.split("\n") if s.strip()]
    return " ".join(sentences[:4])

@traceable(name="news_summary_chain")
def run_summary_chain(instruction: str, feedback: str = "") -> str:
    article = load_news_article()
    prompt = make_prompt(article, instruction, feedback)
    summary = summarize(prompt, article)
    return summary

if __name__ == "__main__":
    instruction = "핵심 문장에 번호를 붙여서 5문장 이내로 요약하세요."
    feedback = "이전 요약은 너무 길었으므로 핵심만 간결하게 정리하세요."
    result = run_summary_chain(instruction=instruction, feedback=feedback)

    print("\n[요약 결과]")
    print(result)
    print("\nLangSmith에서 news_summary_chain run을 확인하세요.")
