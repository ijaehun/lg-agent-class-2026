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

프로젝트 폴더 (`lg-agent-class-2026/`) 안에 **`.env`** 파일을 만들고 아래 한 줄만 적습니다:

```
GEMINI_API_KEY=여기에_복사한_키_붙여넣기
```

⚠️ 따옴표 없이, `=` 양쪽에 공백 없이.
⚠️ `.env` 는 `.gitignore` 에 이미 들어있어서 Git 에 올라가지 않습니다. 안심.

---

## 6. 동작 확인

```bash
python hello.py
```
(Mac 은 `python3 hello.py`)

Gemini 응답이 한 줄 출력되면 **셋업 완료** 🎉

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

해결 안 되는 문제는 강의 첫 회차에 강사에게 문의 주세요.
