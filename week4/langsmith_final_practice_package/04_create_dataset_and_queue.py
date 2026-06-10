import os
from pathlib import Path
from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

PROJECT_NAME = os.getenv("LANGSMITH_PROJECT", "prompt_enhance_example")
DATASET_NAME = PROJECT_NAME
QUEUE_NAME = f"{PROJECT_NAME}_queue"
ARTICLE_PATH = Path("sample_news_article.txt")

def get_or_create_dataset(client: Client, dataset_name: str):
    datasets = list(client.list_datasets(dataset_name=dataset_name))
    if datasets:
        print(f"기존 Dataset 사용: {dataset_name}")
        return datasets[0]

    return client.create_dataset(
        dataset_name=dataset_name,
        description="뉴스 요약 프롬프트 개선 실습용 Dataset",
    )

def create_examples(client: Client, dataset_id):
    article = ARTICLE_PATH.read_text(encoding="utf-8")
    examples = [
        {
            "inputs": {"article": article, "instruction": "핵심 문장에 번호를 붙여 5문장 이내로 요약하세요."},
            "outputs": {"reference_summary": "로컬 LLM, MCP, LangSmith를 결합하면 기업 내부 데이터를 보호하면서 문서 검색, 품질 분석, 실행 모니터링을 수행할 수 있다."},
        },
        {
            "inputs": {"article": article, "instruction": "보안과 생산성 향상 관점만 중심으로 요약하세요."},
            "outputs": {"reference_summary": "로컬 LLM과 MCP를 활용하면 민감한 제조 데이터를 외부 클라우드로 보내지 않고 내부 환경에서 분석할 수 있다."},
        },
    ]

    for i, example in enumerate(examples, start=1):
        try:
            created = client.create_example(
                inputs=example["inputs"],
                outputs=example["outputs"],
                dataset_id=dataset_id,
                metadata={"source": "class_practice", "example_no": i},
            )
            print(f"Example {i} 생성 완료: {created.id}")
        except Exception as e:
            print(f"Example {i} 생성 중 오류 또는 중복 가능성: {e}")

def main():
    client = Client()

    dataset = get_or_create_dataset(client, DATASET_NAME)
    create_examples(client, dataset.id)

    # LangSmith SDK 버전에 따라 queue/rubric API가 변경될 수 있으므로
    # 실패하면 UI에서 Annotation Queue를 생성하면 됩니다.
    try:
        queue = client.create_annotation_queue(
            name=QUEUE_NAME,
            description="뉴스 요약 결과에 대해 사람이 점수, 정답 여부, 피드백을 남기는 큐입니다.",
        )
        print(f"Annotation Queue 생성 완료: {queue.name}")
    except Exception as e:
        print(f"Annotation Queue 생성 중 오류 또는 기존 큐 존재 가능성: {e}")

    print("\nLangSmith UI에서 Dataset과 Annotation Queue를 확인하세요.")
    print("Run은 UI에서 Add to Annotation Queue로 직접 추가하는 방식을 권장합니다.")

if __name__ == "__main__":
    main()
