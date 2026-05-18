"""
실전 데모: 로컬 노트/문서 검색 에이전트.

rag.py 의 "진짜 버전". 하드코딩 DOCS 대신 디스크의 실제 파일을 검색·읽음.
NOTES_DIR 환경변수로 검색 대상 디렉터리 변경 가능 (기본: 현재 폴더).

학습 포인트:
  - 골격은 그대로 (agent loop). 도구만 search_docs → list/read/search 로 교체.
  - ★ 이 파일이 다음 단계의 베이스입니다.
    B반 후반: TOOL_FUNCTIONS + tool_declarations 만 본인 업무 도구로 갈아끼우면
    내 업무용 에이전트가 됨.

실행:
  python notes_agent.py
  NOTES_DIR=C:/Users/이름/Dropbox/notes python notes_agent.py   # Windows
  NOTES_DIR=/Users/이름/Dropbox/notes python3 notes_agent.py    # macOS
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.5-flash"
MAX_TURNS = 10

NOTES_DIR = Path(os.environ.get("NOTES_DIR", ".")).resolve()
ALLOWED_EXTENSIONS = {".md", ".txt", ".py"}
EXCLUDE_DIR_NAMES = {".venv", "__pycache__", "node_modules", ".git"}
MAX_FILE_BYTES = 50_000


# === 도구 1: 파일 목록 ===
def list_files() -> list[str]:
    """검색 가능한 파일 목록을 NOTES_DIR 기준 상대 경로로 반환."""
    out = []
    for path in NOTES_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in ALLOWED_EXTENSIONS:
            continue
        rel = path.relative_to(NOTES_DIR)
        if any(part.startswith(".") or part in EXCLUDE_DIR_NAMES for part in rel.parts):
            continue
        out.append(str(rel).replace("\\", "/"))
    return sorted(out)


# === 도구 2: 파일 읽기 ===
def read_file(path: str) -> str:
    """지정한 파일의 전체 내용을 반환 (50KB 초과 시 잘림)."""
    full = (NOTES_DIR / path).resolve()
    if not full.is_relative_to(NOTES_DIR):
        return f"[오류] 접근 불가 경로: {path}"
    if not full.exists() or not full.is_file():
        return f"[오류] 파일 없음: {path}"
    content = full.read_text(encoding="utf-8", errors="replace")
    if len(content) > MAX_FILE_BYTES:
        cut = len(content) - MAX_FILE_BYTES
        content = content[:MAX_FILE_BYTES] + f"\n\n[...뒤쪽 {cut} 바이트 잘림]"
    return content


# === 도구 3: 키워드 검색 ===
def search_files(keyword: str) -> list[dict]:
    """모든 파일에서 키워드를 찾아 매칭 파일·라인 일부를 반환."""
    results = []
    kw = keyword.lower()
    for filename in list_files():
        full = NOTES_DIR / filename
        try:
            content = full.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if kw not in content.lower():
            continue
        matching_lines = [
            line.strip()
            for line in content.splitlines()
            if kw in line.lower()
        ][:3]
        results.append({"file": filename, "matches": matching_lines})
    return results[:10]


# TODO (1): 이름 → 실제 함수 라우팅 딕셔너리를 채우세요.
#   생각해볼 거리: 이 딕셔너리가 곧 "LLM 이 부른 이름을 우리 함수로 연결" 하는 핵심.
#     본인 업무 도구로 변형할 때 가장 먼저 손대는 자리.
#   힌트: {"list_files": list_files, "read_file": read_file, "search_files": search_files}
TOOL_FUNCTIONS = ___


tool_declarations = [
    {
        "name": "list_files",
        "description": "검색 가능한 노트/문서 파일 전체 목록을 반환. 무엇이 있는지 둘러볼 때.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "read_file",
        "description": "지정한 파일의 전체 내용을 읽어 반환. 자세한 내용이 필요할 때.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "list_files 가 반환한 상대 경로"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "search_files",
        "description": "모든 파일을 훑어 키워드 매칭 결과를 반환. 어디에 무엇이 있는지 찾을 때 먼저 사용.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string", "description": "검색 키워드 (한 단어 권장)"},
            },
            "required": ["keyword"],
        },
    },
]


SYSTEM_INSTRUCTION = (
    f"당신은 로컬 디렉터리({NOTES_DIR}) 의 파일을 검색·읽어서 "
    "사용자 질문에 답하는 도우미입니다. "
    "전략: 어떤 파일이 있는지 모르면 search_files 또는 list_files 로 먼저 살피고, "
    "필요하면 read_file 로 자세히 본 뒤, 그 내용에 근거해서만 답하세요. "
    "파일에 없으면 추측하지 말고 '파일에 없습니다' 라고 답하세요. "
    "답변은 간결하게, 출처 파일명을 함께 적어주세요."
)

config = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[types.Tool(function_declarations=tool_declarations)],
)


def ask(question: str) -> None:
    history = [{"role": "user", "parts": [{"text": question}]}]
    for turn in range(1, MAX_TURNS + 1):
        resp = client.models.generate_content(
            model=MODEL, contents=history, config=config
        )
        content = resp.candidates[0].content
        function_calls = [p.function_call for p in content.parts if p.function_call]

        if not function_calls:
            print(f"\n🤖 {resp.text}\n")
            return

        history.append(content)
        tool_response_parts = []
        for fc in function_calls:
            args = dict(fc.args)
            print(f"  [도구] {fc.name}({args})")
            result = TOOL_FUNCTIONS[fc.name](**args)
            preview = str(result).replace("\n", " ")[:150]
            print(f"  [결과] {preview}{'…' if len(str(result)) > 150 else ''}")
            tool_response_parts.append({
                "function_response": {
                    "name": fc.name,
                    "response": {"result": result},
                }
            })
        history.append({"role": "user", "parts": tool_response_parts})
    print(f"\n[안전 종료] {MAX_TURNS} 턴 초과\n")


if __name__ == "__main__":
    print(f"📂 검색 디렉터리: {NOTES_DIR}")
    print(f"📄 대상 확장자: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
    print("💬 질문을 입력하세요 (빈 줄 또는 'exit' 으로 종료)\n")
    while True:
        try:
            q = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q or q.lower() == "exit":
            break
        ask(q)
