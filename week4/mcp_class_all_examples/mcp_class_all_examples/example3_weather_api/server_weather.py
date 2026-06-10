# example3_weather_api/server_weather.py
# MCP 예제3: 날씨 API MCP 서버
#
# WeatherAPI Key가 있으면 실제 API를 호출합니다.
# Key가 없으면 샘플 날씨 데이터를 반환합니다.

import os
from typing import Any

import requests
from dotenv import load_dotenv
from fastmcp import FastMCP


load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "").strip()
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json"

mcp = FastMCP(
    "WeatherServer",
    instructions="도시 이름을 입력하면 현재 날씨 정보를 반환하는 MCP 서버입니다.",
)


SAMPLE_WEATHER = {
    "Seoul": {
        "city": "Seoul",
        "country": "South Korea",
        "condition": "Clear",
        "temp_c": 25.0,
        "feelslike_c": 26.0,
        "humidity": 55,
        "wind_kph": 8.0,
        "wind_dir": "NW",
        "source": "sample_data",
    },
    "Changwon": {
        "city": "Changwon",
        "country": "South Korea",
        "condition": "Cloudy",
        "temp_c": 24.0,
        "feelslike_c": 25.0,
        "humidity": 65,
        "wind_kph": 10.0,
        "wind_dir": "NE",
        "source": "sample_data",
    },
    "Busan": {
        "city": "Busan",
        "country": "South Korea",
        "condition": "Partly cloudy",
        "temp_c": 23.0,
        "feelslike_c": 24.0,
        "humidity": 60,
        "wind_kph": 12.0,
        "wind_dir": "E",
        "source": "sample_data",
    },
    "London": {
        "city": "London",
        "country": "United Kingdom",
        "condition": "Light rain",
        "temp_c": 15.0,
        "feelslike_c": 14.0,
        "humidity": 78,
        "wind_kph": 14.0,
        "wind_dir": "W",
        "source": "sample_data",
    },
}


@mcp.tool
def get_todays_weather(city_name: str) -> dict[str, Any]:
    """
    특정 도시의 현재 날씨 정보를 조회합니다.

    Args:
        city_name: 도시 이름. 예: Seoul, Changwon, Busan, London
    """
    city_name = city_name.strip()

    if not WEATHER_API_KEY:
        sample = SAMPLE_WEATHER.get(city_name)
        if sample:
            return {
                "status": "success",
                "message": "WEATHER_API_KEY가 없어 샘플 데이터를 사용했습니다.",
                **sample,
            }

        return {
            "status": "error",
            "message": f"{city_name}의 샘플 날씨 데이터가 없습니다. Seoul, Changwon, Busan, London 중 하나를 사용하세요.",
            "source": "sample_data",
        }

    try:
        response = requests.get(
            WEATHER_API_URL,
            params={
                "key": WEATHER_API_KEY,
                "q": city_name,
                "aqi": "no",
            },
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

        location = data.get("location", {})
        current = data.get("current", {})
        condition = current.get("condition", {})

        return {
            "status": "success",
            "city": location.get("name"),
            "country": location.get("country"),
            "localtime": location.get("localtime"),
            "condition": condition.get("text"),
            "temp_c": current.get("temp_c"),
            "feelslike_c": current.get("feelslike_c"),
            "humidity": current.get("humidity"),
            "wind_kph": current.get("wind_kph"),
            "wind_dir": current.get("wind_dir"),
            "source": "weatherapi",
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": "WeatherAPI 호출에 실패했습니다.",
            "detail": str(exc),
        }


if __name__ == "__main__":
    print("Weather MCP Server 실행 중")
    print("접속 주소: http://127.0.0.1:8003/mcp")
    if WEATHER_API_KEY:
        print("WeatherAPI Key가 설정되어 실제 API를 호출합니다.")
    else:
        print("WeatherAPI Key가 없어 샘플 데이터를 사용합니다.")
    print("종료하려면 Ctrl + C")
    mcp.run(transport="http", host="127.0.0.1", port=8003)
