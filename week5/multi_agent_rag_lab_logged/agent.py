"""
Single Agent Controller
- 사용자 요청 해석
- 필요한 tool 선택
- tool 실행 결과를 LLM prompt에 주입
"""

from __future__ import annotations

from typing import List, Dict, Any
import json

from llm import chat
from prompts import SYSTEM_PROMPT, SINGLE_AGENT_PROMPT
from rag import format_evidence_context
from tools import TOOL_REGISTRY
from logger import log_step, log_detail, log_result


def select_tool(user_input: str) -> str:
    """초기 실습용 keyword rule 기반 tool selection."""
    log_step("Single Agent: Tool 선택")
    text = user_input.lower()
    search_keywords = ["문서", "매뉴얼", "근거", "기준", "voc", "가이드", "원인", "결로"]
    log_keywords = ["로그", "시험", "불량률", "습도", "도어", "추이", "ng", "warning"]

    if any(k in text for k in log_keywords):
        log_result("선택된 tool", "analyze_test_log")
        return "analyze_test_log"
    if any(k in text for k in search_keywords):
        log_result("선택된 tool", "search_manual")
        return "search_manual"
    log_result("선택된 tool", "search_manual")
    log_detail("명확한 keyword가 없어 기본 search_manual을 선택합니다.")
    return "search_manual"


def run_agent(user_input: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
    log_step("Single Agent 실행 시작")
    tool_name = select_tool(user_input)
    tool_fn = TOOL_REGISTRY[tool_name]["function"]
    log_step("Single Agent: Tool 호출", tool_name)
    tool_result = tool_fn(user_input)

    if tool_name == "search_manual":
        tool_context = format_evidence_context(tool_result)
    else:
        tool_context = json.dumps(tool_result, ensure_ascii=False, indent=2)

    log_step("Single Agent: Prompt 구성")
    prompt = SINGLE_AGENT_PROMPT.format(user_input=user_input, tool_context=tool_context)
    llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}, *messages, {"role": "user", "content": prompt}]
    log_step("Single Agent: LLM 응답 생성")
    answer = chat(llm_messages)
    log_step("Single Agent 실행 완료")

    return {
        "tool_name": tool_name,
        "tool_result": tool_result,
        "answer": answer,
    }
