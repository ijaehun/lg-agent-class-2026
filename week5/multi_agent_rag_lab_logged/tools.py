"""
업무 Tool 구현 및 Tool Registry
- Agent는 TOOL_REGISTRY에 등록된 tool만 실행한다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, Callable
import json

import pandas as pd

from config import LOG_DIR, OUTPUT_DIR
from rag import search
from logger import log_step, log_detail, log_result


def search_manual(query: str) -> Dict[str, Any]:
    """Reference 문서에서 관련 근거를 검색한다."""
    log_step("Tool 실행", "search_manual")
    return search(query)


def analyze_test_log(query: str) -> Dict[str, Any]:
    """시험 로그 CSV를 읽어 결로/온도/습도 관련 요약 지표를 계산한다."""
    log_step("Tool 실행", "analyze_test_log")
    path = LOG_DIR / "test_log_sample.csv"
    if not path.exists():
        return {"status": "error", "message": f"로그 파일이 없습니다: {path}"}

    log_detail(f"로그 파일 로드: {path}")
    df = pd.read_csv(path)
    log_result("로그 row 수", len(df))
    summary = {
        "row_count": int(len(df)),
        "avg_ambient_humidity": round(float(df["ambient_humidity_pct"].mean()), 2),
        "max_ambient_humidity": round(float(df["ambient_humidity_pct"].max()), 2),
        "avg_door_open_count": round(float(df["door_open_count"].mean()), 2),
        "condensation_ng_count": int((df["condensation_grade"] == "NG").sum()),
        "condensation_warning_count": int((df["condensation_grade"] == "WARNING").sum()),
        "most_common_condition": df["condition"].mode().iloc[0],
    }

    high_risk = df[
        (df["ambient_humidity_pct"] >= 75)
        | (df["door_open_count"] >= 25)
        | (df["condensation_grade"].isin(["WARNING", "NG"]))
    ]

    log_result("NG 건수", summary["condensation_ng_count"])
    log_result("WARNING 건수", summary["condensation_warning_count"])

    return {
        "status": "ok",
        "query": query,
        "summary": summary,
        "high_risk_cases": high_risk.to_dict(orient="records"),
    }


def save_report(markdown_text: str, filename: str = "issue_report.md") -> Dict[str, Any]:
    """보고서 초안을 markdown 파일로 저장한다."""
    log_step("Tool 실행", "save_report")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_filename = filename.replace("/", "_").replace("\\", "_")
    path = OUTPUT_DIR / safe_filename
    path.write_text(markdown_text, encoding="utf-8")
    log_result("저장 경로", path)
    return {"status": "ok", "path": str(path)}


TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "search_manual": {
        "description": "매뉴얼, VOC, 시험 기준 등 reference 문서에서 근거를 검색한다.",
        "function": search_manual,
    },
    "analyze_test_log": {
        "description": "시험 로그 CSV를 분석하여 결로, 습도, 도어 개폐 관련 요약 지표를 계산한다.",
        "function": analyze_test_log,
    },
    "save_report": {
        "description": "최종 보고서 초안을 markdown 파일로 저장한다.",
        "function": save_report,
    },
}


def registry_summary() -> str:
    return json.dumps(
        {name: meta["description"] for name, meta in TOOL_REGISTRY.items()},
        ensure_ascii=False,
        indent=2,
    )
