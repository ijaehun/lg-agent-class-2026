from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
import os

from langchain_community.llms import Ollama
import base64
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

"""
RAG 실습 코드 (이미지 요약 RAG)

- 이미지 파일 로드
  -> VLM을 이용해 이미지 설명 생성
  -> 이미지 설명을 Document로 변환
  -> 이미지 설명 text를 임베딩
  -> FAISS 벡터 저장소 구축
  -> 사용자 질문 입력
  -> 질문과 유사한 이미지 설명 검색
  -> 검색된 이미지 설명을 context로 구성
  -> LLM을 이용한 답변 생성

- 주요 구성
    1. 이미지 로딩
        - ./images/ 폴더에서 jpg, jpeg, png 파일을 읽음
        - 각 이미지 파일의 경로와 파일명을 metadata로 저장

    2. 이미지 설명 생성
        - Llava VLM을 사용하여 이미지 내용을 text description으로 변환
        - 이미지 파일은 base64 문자열로 변환하여 VLM에 전달
        - 생성된 설명은 Document의 page_content에 저장

    3. 벡터 DB 생성
        - OllamaEmbeddings로 이미지 설명 text를 embedding vector로 변환
        - FAISS에 이미지 설명과 metadata를 저장
        - 생성된 벡터 DB는 ./Image_description 경로에 저장

    4. Retriever 검색
        - 사용자 질문을 기준으로 FAISS 벡터 DB에서 관련 이미지 설명 검색
        - 검색된 이미지 설명을 context로 결합
        - source, img_path, description metadata를 통해 원본 이미지와 연결 가능

    5. 이미지 설명 기반 QA
        - 검색된 이미지 설명 context와 사용자 질문을 prompt에 입력
        - LLM이 이미지 설명에 근거하여 답변 생성
        - 설명 안에 답이 없으면 답을 찾을 수 없다고 응답

- 사전 작업
    - Ollama embedding 모델 설치
        ollama pull nomic-embed-text

    - Ollama 생성 모델 설치
        ollama pull llama3.1

    - Llava VLM 모델 설치
        ollama pull llava:7b

    - Python package 설치
        pip install langchain-community
        pip install langchain-ollama
        pip install faiss-cpu

- 실행 전 확인 사항
    - ./images/ 폴더가 존재해야 함
    - ./images/ 폴더 안에 jpg, jpeg, png 이미지가 있어야 함
    - Ollama 서버가 실행 중이어야 함
    - VLM_MODEL은 이미지 입력을 처리할 수 있는 모델이어야 함
        예: llava:7b
    - EMBEDDING_MODEL은 임베딩 전용 모델을 사용해야 함
        예: nomic-embed-text
    - LLM_MODEL은 generate를 지원하는 생성 모델을 사용해야 함
        예: llama3.1

- 참고
    - 이 예제는 이미지를 직접 벡터화하는 방식이 아님
    - 이미지 자체가 아니라 VLM이 생성한 이미지 설명 text를 임베딩함
    - 따라서 검색 품질은 이미지 설명의 품질에 크게 의존함
"""

VECTOR_DB_PATH = "./vector_db/faiss_vector_db"
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.1"
VLM_MODEL = "llava:7b"

IMAGE_PATH = "./images/"
image_files = [f for f in os.listdir(IMAGE_PATH) if f.lower().endswith(('jpg', 'jpeg', 'png'))]

# 이미지 설명용 모델
vlm = OllamaLLM(
    model=VLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0)

# QA용 모델
llm = OllamaLLM(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)

def describe_image(image_path: str) -> str:
    # LLM은 이미지 파일 자체를 입력으로 받을 수 없기 때문에 이미지 파일을 문자열 형태로 변환해서 입력해야 함
    # 이미지를 바이너리로 읽고 base64로 인코딩 후 'utf-8' 문자열로 변환
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
    base64_img = base64.b64encode(img_bytes).decode("utf-8")

    image_summary_prompt = """
    You are an AI assistant specialized in summarizing visual content.
    Please look at the provided image and describe the most important details in a clear and concise manner.
    Do not make assumptions or add imagined details-only describe what is visible.
    Keep the summary to 2-4 sentences.
    """
    result = vlm.invoke(image_summary_prompt, images=[base64_img])
    return result.strip()

# 각 이미지의 설명을 Document에 저장
docs = []
for idx, img_name in enumerate(image_files):
    img_path = os.path.join(IMAGE_PATH, img_name)
    description = describe_image(img_path)
    doc = Document(page_content=description, metadata={"source": img_name, "img_path": img_path, "description": description})
    docs.append(doc)

embedding = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)

# 벡터 스토어 생성
vectorstore = FAISS.from_documents(documents=docs, embedding=embedding)

# 벡터 스토어 저장
vectorstore.save_local("./Image_description")

# Retriever 생성
retriever = vectorstore.as_retriever()

chat_prompt = PromptTemplate.from_template(
    """
    당신은 이미지 설명(Image description)에 기반한 질문-답변(Question-Answering)을 수행하는 AI 어시스턴트입니다.
    당신의 임무는 제공된 이미지에 대한 설명(context)을 바탕으로 사용자의 질문(question)에 답변하는 것입니다.

    아래의 이미지 설명(context)을 참고하여 질문(question)에 답하세요.
    만약 설명 안에 답이 없거나 답을 유추하기 어렵다면, '주어진 이미지 설명에서는 해당 질문에 대한 답을 찾을 수 없습니다' 라고 답하세요.

    # Question:
    {question}

    # Image Description (Context):
    {context}

    # Answer:
    """
)

chat_chain = chat_prompt | llm | StrOutputParser()

# 벡터 DB에서 참고할 문서 검색
question = "사람이 직접 냉장고를 사용하고 있는 모습이 포함된 이미지를 요약해주세요."
retrieved_docs = retriever.invoke(question)
print(f"retrieved size: {len(retrieved_docs)}")
combined_docs = "\n\n".join(doc.page_content for doc in retrieved_docs)

# 검색된 문서를 첨부해서 PROMPT 생성
formatted_prompt = {"context": combined_docs, "question": question}

# 체인을 실행하고 결과를 stream 형태로 출력
print(f"프롬프트:\n{formatted_prompt}")
result = ""
for chunk in chat_chain.stream(formatted_prompt):
    # print(chunk, end="", flush=True)
    result += chunk
print("\n-----------------------------------------")

# 이미지 설명 출력
for doc in retrieved_docs:
    print(f"Source={doc.metadata['source']}\nDescription={doc.metadata['description']}")
