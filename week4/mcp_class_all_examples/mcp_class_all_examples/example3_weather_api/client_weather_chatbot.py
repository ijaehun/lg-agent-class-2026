# example3_weather_api/client_weather_chatbot.py
# MCP 예제3: 날씨 Tool을 사용하는 간단 챗봇
#
# 먼저 아래 서버를 실행해야 합니다.
# python example3_weather_api/server_weather.py

import asyncio
import os
import re
from typing import Any

import requests
from dotenv import load_dotenv
from fastmcp import Client


load_dotenv()

SERVER_URL = "http://127.0.0.1:8003/mcp"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "exaone3.5")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")


WEATHER_KEYWORDS = [
    "날씨", "기온", "온도", "비", "눈", "바람", "습도", "맑음", "흐림",
    "우산", "장마", "태풍", "폭우", "안개", "더워", "추워",
    "weather", "temperature", "rain", "snow", "wind", "sunny", "cloudy",
    "umbrella", "storm", "fog", "humid", "hot", "cold",
]


CITY_MAP = {
    "서울": "Seoul",
    "창원": "Changwon",
    "부산": "Busan",
    "런던": "London",
    "seoul": "Seoul",
    "changwon": "Changwon",
    "busan": "Busan",
    "london": "London",
}


def is_weather_query(text: str) -> bool:
    """사용자 질문이 날씨 관련인지 키워드로 판단합니다."""
    lower = text.lower()
    return any(keyword.lower() in lower for keyword in WEATHER_KEYWORDS)


def detect_language(text: str) -> str:
    """한글 비율로 한국어/영어를 간단히 판별합니다."""
    korean_chars = re.findall(r"[가-힣]", text)
    letters = re.findall(r"[가-힣A-Za-z]", text)

    if not letters:
        return "unknown"

    ratio = len(korean_chars) / len(letters)
    return "korean" if ratio >= 0.3 else "english"


def extract_city_name(text: str) -> str:
    """사용자 질문에서 도시명을 간단히 추출합니다."""
    lower = text.lower()

    for key, value in CITY_MAP.items():
        if key in lower or key in text:
            return value

    match = re.search(r"\bin\s+([A-Za-z ]+)", text)
    if match:
        return match.group(1).strip(" ?.!")

    return "Seoul"


def ollama_generate(prompt: str) -> str | None:
    """Ollama가 켜져 있으면 응답을 생성하고, 아니면 None을 반환합니다."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception:
        return None


def translate_to_english(korean_text: str) -> str:
    """한국어 질문을 영어로 번역합니다. Ollama가 없으면 규칙 기반으로 처리합니다."""
    prompt = f"""
Translate the following Korean sentence into natural English.
Return only the translated sentence.

Korean:
{korean_text}

English:
""".strip()

    result = ollama_generate(prompt)
    if result:
        return result

    city = extract_city_name(korean_text)
    if "우산" in korean_text:
        return f"Do I need an umbrella in {city} today?"
    return f"What is the weather in {city}?"


def translate_to_korean(english_text: str) -> str:
    """영어 답변을 한국어로 번역합니다. Ollama가 없으면 원문을 반환합니다."""
    prompt = f"""
다음 영어 문장을 자연스러운 한국어로 번역하세요.
번역문만 출력하세요.

English:
{english_text}

Korean:
""".strip()

    result = ollama_generate(prompt)
    if result:
        return result

    return english_text


def make_weather_answer(weather: dict[str, Any], user_lang: str) -> str:
    """날씨 Tool 결과를 사용자 답변 문장으로 변환합니다."""
    if weather.get("status") != "success":
        return f"날씨 정보를 가져오지 못했습니다. {weather.get('message')}"

    if user_lang == "korean":
        return (
            f"{weather.get('city')}의 현재 날씨는 {weather.get('condition')}입니다. "
            f"기온은 {weather.get('temp_c')}도, 체감온도는 {weather.get('feelslike_c')}도입니다. "
            f"습도는 {weather.get('humidity')}%, 풍속은 {weather.get('wind_kph')}kph입니다. "
            f"데이터 출처는 {weather.get('source')}입니다."
        )

    return (
        f"The current weather in {weather.get('city')} is {weather.get('condition')}. "
        f"The temperature is {weather.get('temp_c')}°C and feels like {weather.get('feelslike_c')}°C. "
        f"Humidity is {weather.get('humidity')}%, wind speed is {weather.get('wind_kph')} kph. "
        f"Source: {weather.get('source')}."
    )


def answer_general_question(user_input: str, user_lang: str) -> str:
    """날씨가 아닌 일반 질문에 답합니다."""
    result = ollama_generate(f"다음 질문에 짧게 답하세요.\n질문: {user_input}\n답변:")
    if result:
        return result

    if "1+1" in user_input or "1 + 1" in user_input:
        return "1+1은 2입니다." if user_lang == "korean" else "1+1 is 2."

    return "이 질문은 날씨 질문이 아니므로 MCP 날씨 Tool을 호출하지 않았습니다."


async def main():
    client = Client(SERVER_URL)

    async with client:
        tools = await client.list_tools()
        print("사용 가능한 MCP Tool 목록:", [tool.name for tool in tools])

        print("\n날씨 MCP 챗봇 시작")
        print("예시 질문:")
        print("- 서울 날씨 알려줘")
        print("- 오늘 창원 우산 가져가야 하나요?")
        print("- What's the weather in London?")
        print("- 1+1은 뭐야?")
        print("종료: exit")
        print("-" * 70)

        while True:
            user_input = input("\n사용자: ").strip()

            if user_input.lower() in ["exit", "quit", "q"]:
                print("종료합니다.")
                break

            user_lang = detect_language(user_input)
            print(f"[언어 감지] {user_lang}")

            if is_weather_query(user_input):
                print("[질문 분류] 날씨 질문입니다. MCP Tool을 호출합니다.")

                if user_lang == "korean":
                    translated = translate_to_english(user_input)
                    print(f"[한국어 → 영어 변환] {translated}")
                    city_name = extract_city_name(translated)
                else:
                    city_name = extract_city_name(user_input)

                print(f"[Tool 호출] get_todays_weather(city_name='{city_name}')")
                result = await client.call_tool("get_todays_weather", {"city_name": city_name})
                answer = make_weather_answer(result.data, user_lang)

                print("AI:", answer)

            else:
                print("[질문 분류] 날씨 질문이 아닙니다. MCP Tool을 호출하지 않습니다.")
                answer = answer_general_question(user_input, user_lang)
                print("AI:", answer)


if __name__ == "__main__":
    asyncio.run(main())
