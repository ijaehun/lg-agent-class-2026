# 환경 셋업 가이드

이 문서는 **강의 첫 회차 전에 미리 끝내고 오는 사전 자료**입니다.
끝까지 따라 하면 마지막에 `python hello.py` 가 정상 동작하는 것까지 확인합니다.

총 소요 시간: 약 20~30분.

---

## 0. 준비물

- **Python 3.12 이상**
- **코드 에디터** — VS Code 권장 ([code.visualstudio.com](https://code.visualstudio.com))
- **터미널**
  - Windows: PowerShell (시작 메뉴에서 "PowerShell" 검색)
  - macOS: Terminal (Spotlight 에서 "Terminal" 검색)
- **Google 계정** (Gemini API 키 발급용)

---

## 1. Python 설치

### Windows

1. [python.org/downloads](https://www.python.org/downloads/) 에서 **Python 3.12.x** installer 다운로드
2. installer 실행 시 **"Add python.exe to PATH"** 체크박스 반드시 체크 ⚠️
3. "Install Now" 클릭
4. 설치 끝나면 PowerShell 새로 열어서 확인:

   ```powershell
   python --version
   ```

   `Python 3.12.x` 가 나오면 성공.

### macOS

옵션 A — installer 사용 (간단):
1. [python.org/downloads](https://www.python.org/downloads/) 에서 macOS installer 다운로드 후 설치
2. Terminal 새로 열고 확인:

   ```bash
   python3 --version
   ```

옵션 B — Homebrew 사용 (이미 brew 깔린 분):
```bash
brew install python@3.12
python3 --version
```

> **Mac 사용자 주의**: 이후 문서의 `python` 명령은 **`python3`** 으로 바꿔서 입력해주세요.

---

## 2. 강의 자료 받기

### Git 으로 받기 (권장)
```bash
git clone <강의 저장소 URL>
cd lg-agent-class-2026
```

### Zip 으로 받기
GitHub 페이지에서 `Code → Download ZIP` → 압축 해제 → 터미널에서 해당 폴더로 이동
```bash
cd 경로/lg-agent-class-2026
```

---

## 3. 가상환경(venv) 만들기

가상환경 = "이 프로젝트 전용 Python 공간". 강의 패키지가 다른 프로젝트를 오염시키지 않도록 격리합니다.

### 가상환경 생성 (Win / Mac 공통)
```bash
python -m venv .venv
```
(Mac 은 `python3 -m venv .venv`)

`.venv` 폴더가 생기면 성공.

### 가상환경 활성화

**Windows (PowerShell)**:
```powershell
.\.venv\Scripts\Activate.ps1
```

만약 "이 시스템에서 스크립트를 실행할 수 없으므로..." 에러가 나오면 PowerShell 에서 **한 번만** 아래 실행:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
그 다음 다시 활성화 명령 실행.

**macOS**:
```bash
source .venv/bin/activate
```

✅ 프롬프트 앞에 `(.venv)` 가 보이면 활성화 성공.

> 매번 터미널 새로 열 때마다 활성화 명령을 다시 실행해야 합니다.

---

## 4. 의존성 설치

가상환경이 활성화된 상태에서:

```bash
pip install -r requirements.txt
```

`google-genai`, `python-dotenv`, `mcp` 세 패키지가 설치됩니다 (1~2분 소요).

---

## 5. Gemini API 키 발급 + 설정

### (1) API 키 발급
1. [aistudio.google.com/apikey](https://aistudio.google.com/apikey) 접속
2. Google 계정으로 로그인
3. **"Create API key"** 클릭 → 키 복사
4. 키는 `AIzaSy...` 로 시작하는 긴 문자열입니다.

> 무료 tier 로 강의 실습 충분합니다.

### (2) `.env` 파일 만들기

프로젝트 폴더에 이미 **`.env.example`** 이라는 템플릿이 있습니다. 이걸 복사해서 `.env` 로 이름 바꾸세요.

**Windows (PowerShell)**:
```powershell
Copy-Item .env.example .env
```

**macOS**:
```bash
cp .env.example .env
```

그 다음 `.env` 파일을 에디터로 열어서 `your-key-here` 부분을 본인이 발급받은 키로 교체:

```
GEMINI_API_KEY=AIzaSy...본인키...
```

⚠️ 따옴표 없이, `=` 양쪽에 공백 없이.
⚠️ **`.env.example` 에는 키를 넣지 마세요** — 그건 학생 공유용 템플릿이고, 진짜 키는 **`.env`** 에 들어가야 합니다 (`.env` 는 `.gitignore` 처리되어 Git 에 안 올라감).

---

## 6. 동작 확인

```bash
python hello.py
```
(Mac 은 `python3 hello.py`)

Gemini 응답이 한 줄 출력되면 **기본 환경 셋업 완료** 🎉

---

## 7. VS Code 설치

코드를 편집할 에디터입니다. 강의 내내 사용합니다.

### Windows
1. [code.visualstudio.com](https://code.visualstudio.com) 에서 **"Download for Windows"** 클릭 → installer 실행
2. installer 단계에서 다음 옵션 모두 체크 권장:
   - "Add 'Open with Code' action to Windows Explorer file context menu"
   - "Add 'Open with Code' action to Windows Explorer directory context menu"
   - **"Add to PATH"** ⚠️ (터미널에서 `code .` 명령으로 열 수 있게)

### macOS
1. [code.visualstudio.com](https://code.visualstudio.com) 에서 **"Download for Mac"** → zip 다운로드
2. 압축 해제 → `Visual Studio Code.app` 을 **Applications 폴더** 로 드래그
3. (옵션) `Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH" 실행 → 터미널에서 `code .` 사용 가능

### 프로젝트 폴더 열기
```bash
cd lg-agent-class-2026
code .
```
`code` 명령이 안 되면 VS Code 를 직접 실행 → `File → Open Folder` → `lg-agent-class-2026` 폴더 선택.

### (선택) 권장 익스텐션
VS Code 왼쪽 사이드바 **Extensions** (네모 4개 아이콘) 에서:
- **Python** (Microsoft 공식)
- **한국어 언어팩** (Korean Language Pack — 메뉴 한글로 보고 싶은 분만)

---

## 8. GitHub Copilot 가입 + 설치

강의 **Week 0** 에서 "LLM 이 코드를 만들어주는 경험" 을 위해 사용합니다.

### (1) GitHub 계정 + Copilot Free plan 가입

1. GitHub 계정 없으면 [github.com](https://github.com) 에서 가입 (이메일 + 패스워드 + 2FA 권장)
2. 로그인 상태에서 [github.com/features/copilot](https://github.com/features/copilot) 접속
3. **"Get started for free"** 클릭 → 신용카드 필요 없음
4. Copilot Free plan 가입 완료

> **Free plan 한도** (2026년 1월 기준): 월 2,000건 code completion + 50건 chat. 강의용으로 차고 넘침.

### (2) VS Code 익스텐션 설치

1. VS Code 실행
2. 왼쪽 사이드바 **Extensions** (네모 4개 아이콘) 클릭
3. 검색창에 **"GitHub Copilot"** 입력
4. 두 개 모두 설치:
   - **GitHub Copilot** (자동완성)
   - **GitHub Copilot Chat** (채팅 인터페이스)

### (3) 로그인

1. 설치 후 우측 하단에 **"Sign in to GitHub"** 알림 → 클릭
2. 브라우저로 인증 페이지 열림 → **Authorize** 클릭
3. VS Code 로 돌아오면 자동 연결

### (4) 동작 확인

1. VS Code 에서 빈 `.py` 파일 새로 만들기
2. 주석 한 줄 입력: `# 1부터 10까지 더하는 함수`
3. **엔터** 치면 회색 글씨로 코드 제안 보임
4. **Tab** 키로 수락 / **Esc** 로 거절

회색 제안이 뜨면 성공. Week 0 강의에서 본격적으로 체험합니다.

---

## 자주 발생하는 문제

| 증상 | 원인 / 해결 |
|---|---|
| `python: command not found` (Mac) | `python3` 로 입력 |
| `python --version` 이 2.x 로 나옴 (Mac) | `python3 --version` 으로 확인. 이후 명령도 `python3` 사용 |
| `'python' 은(는) 내부 또는 외부 명령...` (Win) | Python 설치 시 PATH 체크 누락. installer 다시 실행해서 "Modify → Add to PATH" 체크 |
| PowerShell 에서 Activate.ps1 실행 거부 | 위 3번의 `Set-ExecutionPolicy` 명령 한 번 실행 |
| `ModuleNotFoundError: No module named 'google'` | 가상환경 활성화 안 됨. 프롬프트에 `(.venv)` 있는지 확인 |
| `KeyError: 'GEMINI_API_KEY'` | `.env` 파일이 프로젝트 폴더에 있는지, 키 이름 오타 없는지 확인 |
| `.env.example` 에 키 넣었는데 동작 안 함 | `.env.example` 은 템플릿. 복사해서 `.env` 로 만든 뒤 그 안에 키 넣어야 함 (위 5번 (2) 참고) |
| `503 UNAVAILABLE` / `experiencing high demand` | Gemini 서버 일시 과부하. 다시 실행하면 보통 통과. 안 되면 1~2분 후 재시도 |
| 터미널에서 `code .` 명령 안 됨 (Win) | VS Code installer 의 "Add to PATH" 체크 누락. installer 재실행해서 옵션 추가 |
| 터미널에서 `code .` 명령 안 됨 (Mac) | VS Code → `Cmd+Shift+P` → "Shell Command: Install 'code' command in PATH" 실행 |
| Copilot 회색 제안이 안 뜸 | ① 우측 하단 Copilot 아이콘 클릭해서 활성 상태인지 확인 ② Sign in 다시 시도 ③ Free plan 가입했는지 확인 |
| GitHub 가입 시 회사 이메일이 보안에 막힘 | 개인 이메일 (Gmail 등) 로 가입 |

해결 안 되는 문제는 강의 첫 회차에 강사에게 문의 주세요.
