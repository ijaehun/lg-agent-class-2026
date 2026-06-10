from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

@traceable(name="classify_question")
def classify_question(question: str) -> str:
    quality_keywords = ["불량", "품질", "개선", "원인", "냉매", "소음"]
    if any(keyword in question for keyword in quality_keywords):
        return "quality_question"
    return "general_question"

@traceable(name="make_answer")
def make_answer(question: str, question_type: str) -> str:
    if question_type == "quality_question":
        return f"'{question}'은 품질 리포트와 관련된 질문입니다. RAG 검색 대상으로 분류됩니다."
    return f"'{question}'은 일반 질문입니다. RAG 검색 없이 처리할 수 있습니다."

@traceable(name="minimal_demo_chain")
def run_demo(question: str) -> str:
    question_type = classify_question(question)
    answer = make_answer(question, question_type)
    return answer

if __name__ == "__main__":
    for q in ["냉매 누설 원인은 뭐야?", "오늘 점심 뭐 먹을까?", "개선 조치는 뭐야?"]:
        print("\n질문:", q)
        print("답변:", run_demo(q))
    print("\nLangSmith 프로젝트에서 trace를 확인하세요.")
