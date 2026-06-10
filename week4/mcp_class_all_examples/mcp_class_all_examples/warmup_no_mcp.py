# warmup_no_mcp.py
# MCP를 사용하기 전에 '도구 함수' 개념을 이해하기 위한 준비 실습입니다.

from pathlib import Path


def add(a: int, b: int) -> int:
    """두 숫자를 더하는 도구 함수입니다."""
    return a + b


def read_quality_report() -> str:
    """샘플 품질 리포트 문서를 읽는 도구 함수입니다."""
    path = Path("sample_data/sample_quality_report.txt")
    return path.read_text(encoding="utf-8")


def ask_document(question: str) -> str:
    """문서를 아주 단순하게 검색해서 답하는 함수입니다."""
    document = read_quality_report()

    if "불량률" in question:
        return "전체 불량률은 2.8%입니다."

    if "원인" in question:
        return "주요 원인 후보는 배관 체결 토크 편차, 신규 작업자 공정 미숙, 특정 협력사 부품 Lot 문제입니다."

    if "개선" in question or "조치" in question:
        return "개선 조치로는 토크 자동 기록 장치 추가, Lot 추적 강화, 입고 검사 기준 상향, 작업자 재교육이 제안되었습니다."

    return "문서에서 관련 내용을 찾지 못했습니다."


print("1. add 함수 실행")
print("10 + 5 =", add(10, 5))

print("\n2. 문서 Q&A 함수 실행")
print("질문: 불량률은 얼마야?")
print("답변:", ask_document("불량률은 얼마야?"))

print("\n질문: 개선 조치는 뭐야?")
print("답변:", ask_document("개선 조치는 뭐야?"))

print("\n핵심:")
print("MCP는 이런 함수를 외부 Client가 표준 방식으로 호출할 수 있게 해주는 구조입니다.")
