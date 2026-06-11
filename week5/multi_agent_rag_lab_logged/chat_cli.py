"""
CLI 실행 파일
- single: Single Agent Controller 실행
- multi: Role-Based Multi-Agent Workflow 실행
"""

from __future__ import annotations

from typing import List, Dict

from agent import run_agent
from multi_agent import run_multi_agent_workflow
from prompts import SYSTEM_PROMPT
from logger import log_step, log_result


def main() -> None:
    print("로컬 RAG + Multi-Agent 실습 CLI")
    print("종료: exit 또는 quit")
    print("mode 선택: single / multi")
    print("실행 중에는 [시간] ▶ 단계명 형식으로 현재 단계 로그가 출력됩니다.")

    mode = input("mode> ").strip().lower()
    if mode not in {"single", "multi"}:
        mode = "multi"
        print("mode가 지정되지 않아 multi로 실행합니다.")

    messages: List[Dict[str, str]] = []

    while True:
        user_input = input("\nuser> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("종료합니다.")
            break
        if not user_input:
            print("빈 입력입니다. 다시 입력하세요.")
            continue

        log_step("사용자 요청 수신")
        log_result("실행 mode", mode)

        if mode == "single":
            result = run_agent(user_input, messages)
            answer = result["answer"]
            print(f"\n[tool: {result['tool_name']}]")
            print(answer)
            messages.append({"role": "user", "content": user_input})
            messages.append({"role": "assistant", "content": answer})
        else:
            result = run_multi_agent_workflow(user_input)
            print("\n[Multi-Agent 최종 결과]")
            print(result["final_report"])
            print("\n[저장 결과]")
            print(result["save_result"])


if __name__ == "__main__":
    main()
