# example1_basic_tools/server_basic_tools.py
# MCP 예제1: 기본 Tool 서버

from pathlib import Path
import base64
import io
from typing import Any

from fastmcp import FastMCP


mcp = FastMCP(
    "BasicToolServer",
    instructions="계산, 현재 폴더 조회, 스크린샷 캡처 기능을 제공하는 실습용 MCP 서버입니다.",
)


@mcp.tool
def add(a: int, b: int) -> dict[str, Any]:
    """두 숫자를 더해서 결과를 반환합니다."""
    return {
        "operation": "add",
        "a": a,
        "b": b,
        "result": a + b,
    }


@mcp.tool
def get_current_dir() -> dict[str, Any]:
    """현재 작업 폴더의 경로와 파일 목록을 반환합니다."""
    current_path = Path.cwd()
    file_list = []

    for item in sorted(current_path.iterdir()):
        file_list.append({
            "name": item.name,
            "type": "directory" if item.is_dir() else "file",
        })

    return {
        "current_path": str(current_path),
        "file_count": len(file_list),
        "files": file_list,
    }


@mcp.tool
def take_screenshot() -> dict[str, Any]:
    """
    현재 화면을 캡처해서 base64 문자열로 반환합니다.
    GUI가 없는 환경에서는 실패할 수 있습니다.
    """
    try:
        import pyautogui

        image = pyautogui.screenshot()
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=70)
        image.save("screenshot_result.jpg")
        image_bytes = buffer.getvalue()

        return {
            "status": "success",
            "format": "jpeg",
            "size_bytes": len(image_bytes),
            "image_base64_first_100_chars": base64.b64encode(image_bytes).decode("utf-8")[:100],
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": "스크린샷 캡처에 실패했습니다. 원격 환경 또는 권한 문제일 수 있습니다.",
            "detail": str(exc),
        }


if __name__ == "__main__":
    print("Basic MCP Server 실행 중")
    print("접속 주소: http://127.0.0.1:8001/mcp")
    print("종료하려면 Ctrl + C")
    mcp.run(transport="http", host="127.0.0.1", port=8001)
