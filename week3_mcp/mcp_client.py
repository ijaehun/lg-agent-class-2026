"""W3 (선택): Gemini 기반 MCP 클라이언트 — 직접 시연용 (베이스라인).

agent_loop.py 변형판 — 도구를 코드에 박지 않고 MCP 서버에서 받아옴.
mcp_server.py 를 subprocess 로 띄워 stdio 로 통신.

흐름:
  1. MCP 서버 subprocess 시작 + session.initialize()
  2. session.list_tools() → MCP 도구 목록 → Gemini function_declarations 로 변환
  3. agent loop (agent_loop.py 와 동일 골격)
     - function_call 오면 session.call_tool() 로 MCP 서버에 위임
     - 결과를 history 에 누적 후 LLM 재호출

실제 사용 시나리오는 Claude Desktop 등록. 이 파일은 "MCP 서버가 동작하는지" 직접 확인용.
"""
import asyncio
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()
gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
MAX_TURNS = 10


def mcp_tool_to_gemini(mcp_tool) -> dict:
    """MCP 도구 정의를 Gemini function_declaration 형식으로 변환."""
    return {
        "name": mcp_tool.name,
        "description": mcp_tool.description or "",
        "parameters": mcp_tool.inputSchema,
    }


async def run_agent(user_question: str, session: ClientSession) -> None:
    # === 1. MCP 서버에서 도구 목록 받아 Gemini 스키마로 변환 ===
    tools_response = await session.list_tools()
    declarations = [mcp_tool_to_gemini(t) for t in tools_response.tools]
    print(f"📡 MCP 서버에서 도구 {len(declarations)}개 받음: {[d['name'] for d in declarations]}\n")

    config = types.GenerateContentConfig(
        system_instruction=(
            "당신은 도구를 사용해 사용자 질문에 답하는 도우미입니다. "
            "필요하면 제공된 도구로 정보를 찾고, 그 결과에 근거해서만 답하세요. "
            "도구 결과에 없는 내용은 추측하지 말고 '문서에 없습니다' 라고 답하세요."
        ),
        tools=[types.Tool(function_declarations=declarations)],
    )

    history = [{"role": "user", "parts": [{"text": user_question}]}]
    print(f"You: {user_question}\n")

    # === 2. Agent loop (agent_loop.py 골격 동일, 도구 실행만 MCP 로 위임) ===
    for turn in range(1, MAX_TURNS + 1):
        print(f"--- turn {turn} ---")
        resp = gemini.models.generate_content(
            model=MODEL, contents=history, config=config
        )
        content = resp.candidates[0].content
        function_calls = [p.function_call for p in content.parts if p.function_call]

        if not function_calls:
            print(f"\nModel: {resp.text}")
            return

        history.append(content)
        tool_response_parts = []
        for fc in function_calls:
            args = dict(fc.args)
            print(f"[MCP 호출] {fc.name}({args})")
            # 핵심: 우리 코드 안에 함수 본체가 없음. MCP 서버에 위임.
            result = await session.call_tool(fc.name, arguments=args)
            result_text = result.content[0].text if result.content else ""
            preview = result_text[:200].replace("\n", " ")
            print(f"[결과]      {preview}{'…' if len(result_text) > 200 else ''}")
            tool_response_parts.append({
                "function_response": {
                    "name": fc.name,
                    "response": {"result": result_text},
                }
            })
        history.append({"role": "user", "parts": tool_response_parts})

    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과")


async def main():
    # MCP 서버를 subprocess 로 띄움 — 현재 Python 인터프리터 (venv) 사용
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await run_agent("신입사원인데 연차 언제부터 쓸 수 있어?", session)


if __name__ == "__main__":
    asyncio.run(main())
