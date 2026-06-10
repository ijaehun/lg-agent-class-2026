# example2_document_qa/client_document_qa.py
# MCP 예제2: 문서 Q&A 클라이언트
#
# 먼저 아래 서버를 실행해야 합니다.
# python example2_document_qa/server_document_qa.py

import asyncio
import json
from pathlib import Path
from typing import Any

from fastmcp import Client


SERVER_URL = "http://127.0.0.1:8002/mcp"
SAMPLE_DOC = Path("sample_data/sample_quality_report.txt")


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

        print_box("업로드할 문서", str(SAMPLE_DOC))

        result = await client.call_tool("upload_document", {"file_path": str(SAMPLE_DOC)})
        print_box("1. 문서 업로드 결과", result.data)

        questions = [
            "이 문서의 전체 불량률은 얼마인가요?",
            "냉매 누설의 원인 후보는 무엇인가요?",
            "개선 조치로 무엇이 제안되었나요?",
        ]

        for question in questions:
            result = await client.call_tool("ask_question", {"query": question, "top_k": 3})
            print_box(f"2. 질문: {question}", result.data)


if __name__ == "__main__":
    asyncio.run(main())
