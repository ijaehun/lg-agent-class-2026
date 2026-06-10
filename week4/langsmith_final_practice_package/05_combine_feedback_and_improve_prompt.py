import json
from pathlib import Path
from dotenv import load_dotenv
from langsmith import traceable

load_dotenv()

FEEDBACK_PATH = Path("sample_feedback.json")

ORIGINAL_PROMPT = '''
당신은 뉴스 요약 AI입니다.
뉴스 원문을 읽고 중요한 내용을 요약하세요.
'''.strip()

@traceable(name="combine_feedback_by_run_id")
def combine_feedback_by_run_id(feedback_list: list[dict]) -> dict:
    new_feedbacks = {}

    for item in feedback_list:
        run_id = str(item.get("run_id"))
        key = item.get("key")
        score = item.get("score")
        comment = item.get("comment", "")

        if run_id not in new_feedbacks:
            new_feedbacks[run_id] = {
                "correctness": "",
                "score": "",
                "notes": "",
            }

        if key == "correctness":
            new_feedbacks[run_id]["correctness"] = score
        elif key == "score":
            new_feedbacks[run_id]["score"] = score
        elif key in ["note", "notes", "comment"]:
            new_feedbacks[run_id]["notes"] = comment

    return new_feedbacks

@traceable(name="convert_feedback_to_xml")
def convert_feedback_to_xml(feedback_by_run: dict) -> str:
    parts = ["<feedbacks>"]

    for run_id, value in feedback_by_run.items():
        parts.append(f'  <feedback run_id="{run_id}">')
        parts.append(f'    <correctness>{value.get("correctness", "")}</correctness>')
        parts.append(f'    <score>{value.get("score", "")}</score>')
        parts.append(f'    <comment>{value.get("notes", "")}</comment>')
        parts.append("  </feedback>")

    parts.append("</feedbacks>")
    return "\n".join(parts)

@traceable(name="make_optimized_prompt")
def make_optimized_prompt(original_prompt: str, feedback_xml: str) -> str:
    optimized_prompt = f'''
당신은 제조 AI 교육용 뉴스 요약 도우미입니다.
아래 뉴스 원문을 읽고 핵심 내용을 5문장 이내로 요약하세요.

[반드시 지킬 규칙]
1. 핵심 문장에는 1, 2, 3처럼 번호를 붙이세요.
2. 원문에 없는 내용은 추가하지 마세요.
3. 서론, 본론, 결론의 흐름이 드러나게 요약하세요.
4. MCP, LangSmith, 로컬 LLM의 역할이 나오면 각각 구분해서 설명하세요.
5. 이전 평가 피드백에서 낮은 점수를 받은 문제를 반복하지 마세요.

[이전 프롬프트]
{original_prompt}

[평가 피드백]
{feedback_xml}

[뉴스 원문]
{{news}}

[요약]
'''.strip()
    return optimized_prompt

def main():
    feedback_list = json.loads(FEEDBACK_PATH.read_text(encoding="utf-8"))

    feedback_by_run = combine_feedback_by_run_id(feedback_list)
    feedback_xml = convert_feedback_to_xml(feedback_by_run)
    optimized_prompt = make_optimized_prompt(ORIGINAL_PROMPT, feedback_xml)

    print("=" * 70)
    print("통합된 feedback XML")
    print("=" * 70)
    print(feedback_xml)

    print("\n" + "=" * 70)
    print("개선된 Prompt")
    print("=" * 70)
    print(optimized_prompt)

    Path("optimized_prompt.txt").write_text(optimized_prompt, encoding="utf-8")
    print("\noptimized_prompt.txt 파일로 저장했습니다.")

if __name__ == "__main__":
    main()
