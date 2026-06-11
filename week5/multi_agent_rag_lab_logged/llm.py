"""
Local LLM 호출 모듈
- 실제 실행: Ollama chat API 사용
- 교육용 데모: USE_MOCK_LLM=True일 때 고정 응답 반환
"""

from __future__ import annotations

from typing import List, Dict
try:
    import ollama
except ImportError:
    ollama = None

from config import CHAT_MODEL, USE_MOCK_LLM
from logger import log_detail, log_result

Message = Dict[str, str]


def chat(messages: List[Message], temperature: float = 0.2) -> str:
    """Ollama local LLM을 호출하고 assistant 응답 문자열을 반환한다."""
    log_result("LLM 입력 message 수", len(messages))
    if USE_MOCK_LLM:
        log_detail("Mock LLM 사용")
        last_user = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return (
            "[MOCK 응답] 입력 요청을 기준으로 문서 근거를 확인하고, "
            "원인 후보와 추가 확인 항목, 보고서 초안을 구조화했습니다.\n\n"
            f"사용자 요청: {last_user[:120]}"
        )

    if ollama is None:
        log_detail("ollama package가 설치되지 않아 오류 안내 응답을 반환합니다.")
        return (
            "[LLM 호출 오류]\n"
            "ollama Python package가 설치되어 있지 않습니다.\n\n"
            "확인 사항:\n"
            "1) `pip install -r requirements.txt`를 실행하세요.\n"
            f"2) `ollama pull {CHAT_MODEL}` 명령으로 모델을 설치하세요.\n"
            "3) 빠른 데모가 필요하면 config.py의 USE_MOCK_LLM=True로 변경하세요."
        )

    try:
        log_detail(f"Ollama LLM 호출: model={CHAT_MODEL}")
        response = ollama.chat(
            model=CHAT_MODEL,
            messages=messages,
            options={"temperature": temperature},
        )
        content = response["message"]["content"]
        log_result("LLM 응답 길이", len(content))
        return content
    except Exception as exc:
        log_detail(f"Ollama 호출 실패: {exc}")
        return (
            "[LLM 호출 오류]\n"
            f"Ollama 모델 호출에 실패했습니다: {exc}\n\n"
            "확인 사항:\n"
            "1) Ollama가 실행 중인지 확인하세요.\n"
            f"2) `ollama pull {CHAT_MODEL}` 명령으로 모델을 설치하세요.\n"
            "3) 빠른 데모가 필요하면 config.py의 USE_MOCK_LLM=True로 변경하세요."
        )
