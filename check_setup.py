"""환경 셋업 검증 스크립트 (강의 코드 아님).

SETUP.md 의 1~5 단계를 마친 뒤 실행하세요.
패키지 import + API 키 로드 + Gemini 호출까지 한 번에 점검합니다.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai


def main() -> None:
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[X] .env 파일에 GEMINI_API_KEY 가 없습니다. SETUP.md 5번 다시 확인.")
        sys.exit(1)

    print("[OK] 패키지 import")
    print("[OK] .env 의 API 키 로드")

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="한 줄로 '셋업 OK' 라고 답해줘",
        )
        print(f"[OK] Gemini 응답: {response.text.strip()}")
        print("\n환경 셋업 완료. 첫 회차에서 만나요.")
    except Exception as e:
        print(f"[X] API 호출 실패: {e}")
        print("SETUP.md 의 '자주 발생하는 문제' 표 확인.")
        sys.exit(1)


if __name__ == "__main__":
    main()
