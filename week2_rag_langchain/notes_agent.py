"""W2 + W3 통합 실전판: 노트 도우미 에이전트 (베이스라인).

도구 3개 (list, read, search) 가 협업. NOTES_DIR 환경변수로 본인 폴더 가능.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-3.5-flash"
MAX_TURNS = 10

DEFAULT_NOTES_DIR = Path(__file__).parent.parent / "notes"
NOTES_DIR = Path(os.environ.get("NOTES_DIR", str(DEFAULT_NOTES_DIR))).resolve()
ALLOWED_EXTENSIONS = {".md", ".txt"}
EXCLUDE_DIR_NAMES = {".venv", "__pycache__", "node_modules", ".git"}
MAX_FILE_BYTES = 50_000


def list_notes() -> list[str]:
    out = []
    for path in NOTES_DIR.rglob("*"):
        if not path.is_file() or path.suffix not in ALLOWED_EXTENSIONS:
            continue
        rel = path.relative_to(NOTES_DIR)
        if any(part.startswith(".") or part in EXCLUDE_DIR_NAMES for part in rel.parts):
            continue
        out.append(str(rel).replace("\\", "/"))
    return sorted(out)


def read_note(filename: str) -> str:
    full = (NOTES_DIR / filename).resolve()
    if not full.is_relative_to(NOTES_DIR):
        return f"[오류] 접근 불가 경로: {filename}"
    if not full.exists() or not full.is_file():
        return f"[오류] 파일 없음: {filename}"
    content = full.read_text(encoding="utf-8", errors="replace")
    if len(content) > MAX_FILE_BYTES:
        cut = len(content) - MAX_FILE_BYTES
        content = content[:MAX_FILE_BYTES] + f"\n\n[...뒤쪽 {cut} 바이트 잘림]"
    return content


def search_notes(keyword: str) -> list[dict]:
    results = []
    kw = keyword.lower()
    for filename in list_notes():
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


TOOL_FUNCTIONS = {
    "list_notes": list_notes,
    "read_note": read_note,
    "search_notes": search_notes,
}

tool_declarations = [
    {
        "name": "list_notes",
        "description": "검색 가능한 노트 파일 전체 목록을 반환. 무엇이 있는지 둘러볼 때 사용.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "name": "read_note",
        "description": "지정한 노트 파일의 전체 내용을 읽어 반환. 자세한 내용이 필요할 때.",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "list_notes 가 반환한 상대 경로"},
            },
            "required": ["filename"],
        },
    },
    {
        "name": "search_notes",
        "description": "모든 노트를 훑어 키워드 매칭 결과를 반환. 어디에 무엇이 있는지 찾을 때 먼저 사용.",
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
    f"당신은 로컬 노트 폴더({NOTES_DIR}) 의 파일을 검색·읽어서 "
    "사용자 질문에 답하는 도우미입니다. "
    "전략: 어떤 파일이 있는지 모르면 search_notes 또는 list_notes 로 먼저 살피고, "
    "필요하면 read_note 로 자세히 본 뒤, 그 내용에 근거해서만 답하세요. "
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
        resp = client.models.generate_content(model=MODEL, contents=history, config=config)
        content = resp.candidates[0].content
        function_calls = [p.function_call for p in content.parts if p.function_call]

        if not function_calls:
            print(f"\n[답변] {resp.text}\n")
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
    print(f"노트 폴더: {NOTES_DIR}")
    print(f"대상 확장자: {', '.join(sorted(ALLOWED_EXTENSIONS))}")
    print("질문을 입력하세요 (빈 줄 또는 'exit' 으로 종료)\n")
    while True:
        try:
            q = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not q or q.lower() == "exit":
            break
        ask(q)
