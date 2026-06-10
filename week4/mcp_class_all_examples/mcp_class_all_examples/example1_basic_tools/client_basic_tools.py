# example1_basic_tools/client_basic_tools.py
# MCP 예제1: 기본 Tool 클라이언트
#
# 먼저 아래 서버를 실행해야 합니다.
# python example1_basic_tools/server_basic_tools.py

import asyncio
import json
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8001/mcp"


def print_box(title: str, data: Any):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    if isinstance(data, (dict, list)):
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(data)


async def main():
    client = Client(SERVER_URL)

    async with client:
        tools = await client.list_tools()
        print_box("서버에 등록된 MCP Tool 목록", [tool.name for tool in tools])

        result = await client.call_tool("add", {"a": 10, "b": 5})
        print_box("1. add Tool 실행 결과", result.data)

        result = await client.call_tool("get_current_dir", {})
        print_box("2. get_current_dir Tool 실행 결과", result.data)

        result = await client.call_tool("take_screenshot", {})
        print_box("3. take_screenshot Tool 실행 결과", result.data)


if __name__ == "__main__":
    asyncio.run(main())
