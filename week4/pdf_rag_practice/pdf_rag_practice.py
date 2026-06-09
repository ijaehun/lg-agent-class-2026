from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
import os

"""
RAG 실습 코드 (Basic PDF RAG)

- PDF 문서 로드
  -> 문서 분할
  -> 임베딩
  -> FAISS 벡터 저장소 구축
  -> 사용자 질문 입력
  -> 벡터 DB에서 관련 문서 검색
  -> 검색된 문서를 context로 구성
  -> context와 질문을 프롬프트에 입력
  -> LLM을 이용한 답변 생성

- 주요 구성
    1. PDF 문서 로딩
        - PyPDFLoader로 PDF 파일을 페이지 단위 Document로 변환
        - 각 Document는 page_content와 metadata를 포함

    2. 문서 분할
        - RecursiveCharacterTextSplitter로 긴 문서를 작은 chunk로 분할
        - chunk_size와 chunk_overlap을 조정하여 검색 단위를 설정

    3. 벡터 DB 생성
        - OllamaEmbeddings로 각 chunk를 embedding vector로 변환
        - FAISS에 embedding vector와 문서 chunk를 저장
        - 생성된 벡터 DB는 로컬 경로에 저장하여 재사용

    4. Retriever 검색
        - 사용자 질문을 기준으로 벡터 DB에서 관련 chunk 검색
        - 검색된 chunk들을 하나의 context로 결합

    5. RAG 답변 생성
        - 검색된 context와 사용자 질문을 prompt에 입력
        - OllamaLLM을 사용하여 문서 기반 답변 생성

- 사전 작업
    - Ollama embedding 모델 설치
        ollama pull nomic-embed-text

    - Ollama 생성 모델 설치
        ollama pull llama3.1

    - Python package 설치
        pip install PyMuPDF
        pip install langchain-community
        pip install faiss-cpu
        pip install langchain-ollama
        pip install langchain-text-splitters

- 실행 전 확인 사항
    - ./document/weather_news.pdf 파일이 존재해야 함
    - Ollama 서버가 실행 중이어야 함
    - EMBEDDING_MODEL은 임베딩 전용 모델을 사용해야 함
        예: nomic-embed-text
    - LLM_MODEL은 generate를 지원하는 생성 모델을 사용해야 함
        예: llama3.1

- 종료 방법
    - 질문 입력창에 "끝" 또는 "exit" 입력
"""

VECTOR_DB_PATH = "./vector_db/faiss_vector_db"
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.1"

# 1. 벡터 DB 파일이 없으면 생성 후 vector_store 반환
def create_vector_db():
    # 1-1. 문서 로딩 (Document Loading)
    loader = PyPDFLoader("./document/weather_news.pdf")
    docs = loader.load()
    print(f"문서의 수: {len(docs)}")

    # 1-2. 문서 분할 (Splitting)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=70)
    splits = text_splitter.split_documents(docs)

    # 1-3. 임베딩 생성 (Embedding)
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)

    # 1-4. 벡터 저장소 구축 (Vector Database)
    vector_store = FAISS.from_documents(documents=splits, embedding=embeddings)

    # 1-5. 벡터 DB를 로컬에 저장
    vector_store.save_local(VECTOR_DB_PATH)

    return vector_store

# 2. 메인 로직
if os.path.exists(VECTOR_DB_PATH):
    # 벡터 DB 파일이 존재하면 로드
    print("기존 벡터 DB를 로드합니다.")
    embeddings = OllamaEmbeddings(model="EMBEDDING_MODEL", base_url=OLLAMA_BASE_URL)
    # 로컬 경로에서 벡터 DB를 불러오고, 지정된 임베딩 객체를 사용해 벡터를 처리
    # allow_dangerous_deserialization=True 옵션은 로컬 파일에서 벡터 DB를 불러올 때, 신뢰할 수 있는 소스임을 확인한 경우에만 사용해야 하는 옵션임.
    # 이 옵션을 사용하면 보안 위험이 있을 수 있으므로, 반드시 신뢰할 수 있는 파일에서만 사용해야 함.
    vector_store = FAISS.load_local(VECTOR_DB_PATH, 
                                    embeddings,
                                    allow_dangerous_deserialization=True # 믿을 수 있는 소스임을 확인
                                    )
else:
    print("새로운 벡터 DB를 생성합니다.")
    vector_store = create_vector_db()

# 3-1. 쿼리 저장소 검색을 위한 retriever 생성
retriever = vector_store.as_retriever()

while True:
    question = input("\n\n당신: ")
    if question == "끝" or question == "exit":
        print("대화를 종료합니다.")
        break
    
    retrieved_docs = retriever.invoke(question)
    print(f"retrieved size: {len(retrieved_docs)}")
    combined_docs = "\n\n".join([doc.page_content for doc in retrieved_docs])

    formatted_prompt = {"context": combined_docs, "question": question}
    llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
    prompt = ChatPromptTemplate.from_template(
        """다음 컨텍스트를 기반으로 질문에 답변해주세요.
        컨텍스트:
        {context}

        질문: {question}

        답변:"""
    )

    chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # 7. LLM을 이용한 답변 생성
    print("LLM이 생성한 답변:")
    for chunk in chain.stream(formatted_prompt):
        print(chunk, end="", flush=True)
