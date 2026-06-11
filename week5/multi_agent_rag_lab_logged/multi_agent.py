"""
Role-Based Multi-Agent Workflow
- MCP 없이, RAG와 Tool Registry를 기반으로 multi-agent의 큰 구조를 학습하기 위한 코드
- 각 agent는 하나의 역할만 담당하고, 다음 agent에게 중간 산출물을 넘긴다.
"""

from __future__ import annotations

from typing import Dict, Any
import json

from llm import chat
from prompts import (
    SYSTEM_PROMPT,
    SEARCH_AGENT_PROMPT,
    ANALYSIS_AGENT_PROMPT,
    WRITER_AGENT_PROMPT,
    REVIEWER_AGENT_PROMPT,
)
from rag import format_evidence_context
from tools import search_manual, analyze_test_log, save_report
from logger import log_step, log_detail, log_result


def call_role_agent(role_prompt: str) -> str:
    log_detail("LLM 호출 준비")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": role_prompt},
    ]
    result = chat(messages)
    log_detail("LLM 응답 수신")
    return result


def search_agent(user_input: str) -> Dict[str, Any]:
    log_step("Multi-Agent 1/4: Search Agent 실행")
    evidence_packet = search_manual(user_input)
    prompt = SEARCH_AGENT_PROMPT.format(
        user_input=user_input,
        evidence_context=format_evidence_context(evidence_packet),
    )
    log_detail("Search Agent prompt 구성 완료")
    result = call_role_agent(prompt)
    log_result("Search Agent 근거 여부", evidence_packet.get("has_context"))
    return {
        "agent": "search_agent",
        "evidence_packet": evidence_packet,
        "result": result,
    }


def analysis_agent(user_input: str, search_output: Dict[str, Any]) -> Dict[str, Any]:
    log_step("Multi-Agent 2/4: Analysis Agent 실행")
    test_log_result = analyze_test_log(user_input)
    prompt = ANALYSIS_AGENT_PROMPT.format(
        user_input=user_input,
        search_result=search_output["result"],
        log_result=json.dumps(test_log_result, ensure_ascii=False, indent=2),
    )
    log_detail("Analysis Agent prompt 구성 완료")
    result = call_role_agent(prompt)
    log_result("Analysis Agent 로그 분석 상태", test_log_result.get("status"))
    return {
        "agent": "analysis_agent",
        "log_result": test_log_result,
        "result": result,
    }


def writer_agent(user_input: str, analysis_output: Dict[str, Any]) -> Dict[str, Any]:
    log_step("Multi-Agent 3/4: Writer Agent 실행")
    prompt = WRITER_AGENT_PROMPT.format(
        user_input=user_input,
        analysis_result=analysis_output["result"],
    )
    log_detail("Writer Agent prompt 구성 완료")
    draft = call_role_agent(prompt)
    log_result("Writer Agent 초안 길이", len(draft))
    return {
        "agent": "writer_agent",
        "draft_report": draft,
    }


def reviewer_agent(user_input: str, writer_output: Dict[str, Any]) -> Dict[str, Any]:
    log_step("Multi-Agent 4/4: Reviewer Agent 실행")
    prompt = REVIEWER_AGENT_PROMPT.format(
        user_input=user_input,
        draft_report=writer_output["draft_report"],
    )
    log_detail("Reviewer Agent prompt 구성 완료")
    review = call_role_agent(prompt)
    log_result("Reviewer Agent 검토문 길이", len(review))
    return {
        "agent": "reviewer_agent",
        "review": review,
    }


def run_multi_agent_workflow(user_input: str, save: bool = True) -> Dict[str, Any]:
    """검색 → 분석 → 작성 → 검토 순서의 고정 workflow."""
    log_step("Multi-Agent Workflow 시작")
    search_output = search_agent(user_input)
    analysis_output = analysis_agent(user_input, search_output)
    writer_output = writer_agent(user_input, analysis_output)
    reviewer_output = reviewer_agent(user_input, writer_output)

    log_step("Multi-Agent: 최종 보고서 조합")
    final_report = (
        writer_output["draft_report"]
        + "\n\n---\n\n"
        + reviewer_output["review"]
    )

    save_result = save_report(final_report) if save else {"status": "skipped"}
    log_step("Multi-Agent Workflow 완료")

    return {
        "user_input": user_input,
        "search_output": search_output,
        "analysis_output": analysis_output,
        "writer_output": writer_output,
        "reviewer_output": reviewer_output,
        "final_report": final_report,
        "save_result": save_result,
    }


if __name__ == "__main__":
    sample_request = "도어 결로 VOC와 시험 로그를 참고해서 원인 후보, 추가 확인 항목, 고객 대응 초안을 정리해줘."
    result = run_multi_agent_workflow(sample_request)
    print(result["final_report"])
    print("\n저장 결과:", result["save_result"])
