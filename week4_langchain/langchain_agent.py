"""
Week 4: LangChain — agent_loop.py 와 같은 일을 한 줄로.

학습 목표:
  - W2 의 agent_loop.py 와 똑같은 결과 (날씨 + 옷 추천) 를 LangChain 으로 짠다
  - 우리가 직접 짠 100줄 골격이 = create_react_agent 한 줄 임을 눈으로 본다
  - "LangChain 도 결국 우리 골격 위의 편의 기능" 이 손에 잡힌다

실행:
  python langchain_agent.py
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()


# === 도구 정의 ===
# TODO (1): 아래 두 함수 위에 LangChain 의 @tool 데코레이터를 추가하세요.
#   생각해볼 거리: 이 데코레이터가 자동으로 만들어주는 것은?
#     - 함수 시그니처 → tool schema
#     - docstring → tool description
#   힌트: @tool

___
def get_weather(city: str) -> dict:
    """주어진 도시의 현재 날씨와 기온(섭씨)을 반환한다."""
    data = {
        "서울": {"condition": "맑음", "temp_celsius": 22},
        "부산": {"condition": "흐림", "temp_celsius": 25},
        "제주": {"condition": "비", "temp_celsius": 18},
    }
    return data.get(city, {"condition": "알 수 없음", "temp_celsius": 0})


___
def recommend_outfit(temp_celsius: int) -> str:
    """현재 기온(섭씨)에 따라 적절한 옷차림을 추천한다."""
    if temp_celsius >= 25:
        return "반팔 + 반바지"
    elif temp_celsius >= 15:
        return "긴팔 + 청바지"
    else:
        return "패딩 + 목도리"


# === LLM (Gemini) 연결 ===
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.environ["GEMINI_API_KEY"],
)


# TODO (2): create_react_agent 한 줄로 agent 만들기.
#   생각해볼 거리: 이 한 줄 안에 W2 agent_loop.py 의 무엇이 들어있을까?
#     - while 루프? function_call 처리? function_response 형식? MAX_TURNS?
#   힌트: create_react_agent(llm, tools=[get_weather, recommend_outfit])
agent = ___


if __name__ == "__main__":
    user_question = "서울 날씨 보고 오늘 뭐 입을지 추천해줘"
    print(f"You: {user_question}\n")

    result = agent.invoke({"messages": [("user", user_question)]})

    # 전체 흐름 출력 — 어떤 도구가 호출되고 어떤 결과를 받았는지 보임
    for msg in result["messages"]:
        msg.pretty_print()
