"""
콘솔 로그 유틸리티
- 수강생이 현재 어떤 단계가 실행되는지 확인할 수 있도록 공통 로그 함수를 제공한다.
- 핵심 로직에는 영향을 주지 않고 print 출력만 담당한다.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


LOG_ENABLED = True


def log_step(step: str, message: str = "") -> None:
    """큰 실행 단계를 출력한다."""
    if not LOG_ENABLED:
        return
    now = datetime.now().strftime("%H:%M:%S")
    suffix = f" - {message}" if message else ""
    print(f"\n[{now}] ▶ {step}{suffix}")


def log_detail(message: str) -> None:
    """세부 실행 정보를 출력한다."""
    if not LOG_ENABLED:
        return
    print(f"    - {message}")


def log_result(label: str, value: Any) -> None:
    """짧은 결과 요약을 출력한다."""
    if not LOG_ENABLED:
        return
    print(f"    → {label}: {value}")
