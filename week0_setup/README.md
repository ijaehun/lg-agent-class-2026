# Week 0 — 환경 셋업 + Copilot 체험

본 강의 (4주) 시작 전 **사전 단발 세션** 입니다. 1.5시간.
다음 회차부터의 실습이 매끄럽게 굴러가도록 환경을 다 같이 점검하고, 첫 LLM 체험을 합니다.

## 이번 시간에 할 것

1. **환경 점검** (사전에 `SETUP.md` 따라온 분 기준)
   - `python hello.py` 가 실제로 응답을 받아오는지 확인
   - 안 되는 분 — 다 같이 잡고 갑니다
2. **GitHub Copilot 설치 + 첫 체험**
   - VS Code 에 Copilot 깔기
   - 빈 파일에 주석만 적어도 코드가 만들어지는 마법(?)을 본다
3. **핵심 메시지 한 가지**
   - "Copilot 도 결국 LLM 한 번 호출. 다음 주부터 그 본질을 우리가 직접 만들어볼 것."

## 마치고 나면 (체크리스트)

- [ ] `.venv` 활성화 상태에서 `python hello.py` 가 동작한다
- [ ] VS Code 의 Copilot 익스텐션이 활성 (오른쪽 아래에 Copilot 아이콘 보임)
- [ ] `copilot_play.py` 의 주석에서 Copilot 이 코드를 제안한 경험이 있다

---

## (1) 사전 작업 — 강의 전에 끝내고 오세요

`SETUP.md` 의 1~6 단계까지 따라 하면 끝입니다.
끝까지 가서 `python hello.py` 가 응답을 한 줄 출력하는 것까지 확인해주세요.

안 되면 그대로 강의에 와도 됩니다. **다 같이 잡고 가는 시간** 이 회차의 절반입니다.

---

## (2) Copilot 설치 안내

### a. GitHub 계정 + Copilot Free plan 가입

1. GitHub 계정이 없으면 [github.com](https://github.com) 에서 가입 (이메일 + 패스워드)
2. 로그인 상태에서 [github.com/features/copilot](https://github.com/features/copilot) 접속
3. **"Get started for free"** 클릭 — 신용카드 필요 없음
4. Copilot Free plan 가입 완료

> **Free plan 한도** (2026년 1월 기준): 월 2,000건 code completion + 50건 chat. 강의 한 회차엔 차고 넘칩니다.

### b. VS Code 익스텐션 설치

1. VS Code 실행
2. 왼쪽 사이드바의 **Extensions** (네모 4개 아이콘) 클릭
3. 검색창에 **"GitHub Copilot"** 입력
4. 두 개 모두 설치:
   - **GitHub Copilot** (자동완성)
   - **GitHub Copilot Chat** (채팅 인터페이스)
5. 설치 후 우측 하단에 "Sign in to GitHub" 알림 → 클릭해서 로그인

### c. 동작 확인

- VS Code 오른쪽 아래에 Copilot 아이콘이 보이면 OK
- 호버하면 "Copilot is ready" 같은 메시지

---

## (3) 첫 체험: copilot_play.py

`week0_setup/copilot_play.py` 를 열고 강의 진행에 따라 함께 실습합니다.
빈 파일에 **주석 한 줄** 만 적어도 Copilot 이 코드를 제안해줄 거예요.

학생이 미리 풀어보고 와도 좋습니다. 단, 결과물이 모두 다르게 나옵니다 — **그게 이번 시간의 포인트**.
1주차 본 실습부터는 동일 결과를 위해 starter 코드를 따라갑니다.

---

## 다음 회차 (Week 1) 예고

다음 시간에는 Copilot 없이 우리가 직접 `hello.py` 의 정체를 분해해봅니다.
"방금 Copilot 이 우리에게 코드를 만들어준 그 과정" 의 가장 작은 단위가 무엇인지 직접 손으로 짜봅니다.
