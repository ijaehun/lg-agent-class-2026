# Week 4 — MCP 표준

이번 주의 메시지:

> **MCP = 도구의 USB-C.**
>
> 지금까지는 도구를 짤 때마다 `tool_declarations` 를 그 코드 안에 박아넣었습니다.
> MCP 는 이 도구를 **외부에 표준 단자로 노출** 합니다.
> → 같은 도구를 Claude Desktop / Cursor / 우리 에이전트 어디든 꽂을 수 있음.

## 학습 목표

- `rag.py` 의 `search_docs` 와 **로직은 똑같다**. 차이는 `@mcp.tool()` 데코레이터 하나.
- MCP 서버를 직접 짜본다 (`mcp_server.py`)
- **Claude Desktop 에 등록** 해서 진짜 클라이언트가 우리 도구를 부르는 것을 본다 ← 이번 주 하이라이트

## 파일

| 파일 | 내용 |
|---|---|
| `mcp_server.py` | rag.py 의 search_docs 를 MCP 도구로 노출 — 빈칸 2곳 채우기 |

> async 클라이언트 예시(`mcp_client.py`)는 옵션 자료입니다. 시간 남으면 `../solutions/week4_mcp/mcp_client.py` 를 열어 보세요.

## 단계별 진행

### 1. 빈칸 채우고 서버 단독 실행 확인

```bash
python mcp_server.py
```

실행하면 출력 없이 멈춰있는 것처럼 보입니다 — **정상**. stdio 로 클라이언트의 연결을 기다리는 상태.
`Ctrl+C` 로 종료.

### 2. Claude Desktop 에 등록

**(a) Claude Desktop 설치** (이미 깔려 있으면 건너뜀):
[claude.ai/download](https://claude.ai/download) 에서 다운로드.

**(b) 설정 파일 위치**:

| OS | 경로 |
|---|---|
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |

> 파일이 없으면 새로 만드세요. Claude Desktop 의 `Settings → Developer → Edit Config` 버튼으로도 열 수 있습니다.

**(c) 아래 내용을 추가** — 경로는 본인 환경으로 바꿔주세요:

Windows:
```json
{
  "mcpServers": {
    "company-wiki": {
      "command": "C:\\Users\\이름\\Dropbox\\github\\lg-agent-class-2026\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\이름\\Dropbox\\github\\lg-agent-class-2026\\week4_mcp\\mcp_server.py"]
    }
  }
}
```

macOS:
```json
{
  "mcpServers": {
    "company-wiki": {
      "command": "/Users/이름/lg-agent-class-2026/.venv/bin/python3",
      "args": ["/Users/이름/lg-agent-class-2026/week4_mcp/mcp_server.py"]
    }
  }
}
```

⚠️ **중요**:
- `command` 는 **venv 안의 python** 을 써야 `mcp` 패키지가 잡힙니다 (시스템 python 이면 모듈 못 찾음).
- 경로는 **절대 경로** 로 입력.
- Windows JSON 의 `\` 는 두 개 (`\\`) 로 써야 함.

**(d) Claude Desktop 재시작** → 새 채팅 창의 도구 아이콘에 `company-wiki` 가 보이면 성공.

**(e) 테스트 프롬프트**:
```
신입사원인데 연차 언제부터 쓸 수 있어?
```
→ Claude 가 `search_docs` 호출 → 우리 mcp_server 가 응답 → Claude 가 자연어로 답.

## 끝나면 (B반 후반 — 본인 자동화 데모)

3주차에 만든 본인 업무 도구를 MCP 서버로 노출 → Claude Desktop 에 등록 → 본인 업무에서 실제로 사용.
**= 4주짜리 강의의 결실.**

## 강의 마무리 메시지

> 여러분이 이번 4주에 배운 게 곧 에이전트의 전부입니다.
> LangChain · CrewAI 는 우리가 짠 골격 위의 편의 기능일 뿐이고,
> 실무 자동화 = **같은 골격 + 회사에 맞는 도구** 입니다.
