from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
import os

"""
RAG 실습 코드 (Advanced RAG: Multi-Query Retrieval + Context Compression)

- PDF 문서 로드
  -> 문서 분할
  -> 임베딩
  -> FAISS 벡터 저장소 구축
  -> 사용자 질문 입력
  -> LLM을 이용한 변형 질문 생성
  -> 여러 질문으로 벡터 DB 검색
  -> 검색 결과 통합 및 중복 제거
  -> 검색 문서 압축(Context Compression)
  -> 압축된 컨텍스트를 기반으로 최종 답변 생성

- 주요 구성
    1. Vector DB 생성
        - PyPDFLoader로 PDF 문서 로드
        - RecursiveCharacterTextSplitter로 문서 chunk 분할
        - OllamaEmbeddings로 chunk 임베딩
        - FAISS에 벡터 저장

    2. Multi-Query Retrieval
        - 사용자 질문을 LLM이 여러 개의 변형 질문으로 paraphrasing
        - 각 변형 질문으로 벡터 DB 검색
        - 검색된 문서를 하나로 통합
        - 중복 문서 제거

    3. Context Compression
        - 검색된 여러 문서 중 질문과 관련된 핵심 정보만 추출
        - 불필요하거나 중복된 문맥 제거
        - 최종 QA에 사용할 압축된 context 생성

    4. Final QA
        - 압축된 context와 원본 질문을 QA prompt에 입력
        - LLM이 근거 기반 답변 생성

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
    - ./document/원자력안전관리_설명자료.pdf 파일이 존재해야 함
    - Ollama 서버가 실행 중이어야 함
    - EMBEDDING_MODEL은 임베딩 전용 모델을 사용해야 함
        예: nomic-embed-text
    - LLM_MODEL은 generate를 지원하는 생성 모델을 사용해야 함
        예: llama3.1
"""


VECTOR_DB_PATH = "faiss_index"
LLM_MODEL = "llama3.1"
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"


# 벡터 DB 생성
def create_vector_db():
    # Document 폴더에서 pdf 호출
    loader = PyPDFLoader("./document/원자력안전관리_설명자료.pdf")
    docs = loader.load()
    print(f"문서의 수: {len(docs)}")

    # 문서를 일정 길이 (chunk_size)로 나눔
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    print(f"split size: {len(splits)}")

    # 텍스트 조각을 벡터 임베딩
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
        )

    # 분할된 텍스트를 임베딩 후 FAISS 벡터 저장소를 생성하고 로컬 디스크에 저장
    vector_store = FAISS.from_documents(
        documents=splits,
        embedding=embeddings
    )
    vector_store.save_local(VECTOR_DB_PATH)
    return vector_store

def generate_multiple_queries(question, llm, num_queries=7):
    
    chain = multi_query_prompt | llm | StrOutputParser()

    result = chain.invoke({
        "question": question
    })

    queries = [line.strip() for line in result.splitlines() if line.strip()]

    cleaned_queries = []

    for q in queries:
        # 번호, 불릿 제거
        q = q.lstrip("0123456789. )-•")
        q = q.strip()

        if q:
            cleaned_queries.append(q)

    # 원본 질문도 검색에 포함
    final_queries = [question] + cleaned_queries

    # 중복 제거
    unique_queries = []
    seen = set()

    for q in final_queries:
        if q not in seen:
            unique_queries.append(q)
            seen.add(q)

    return unique_queries[:num_queries]


def compress_context(question, docs, llm):

    documents_text = "\n\n".join(
        [
            f"[문서 {i+1} | page: {doc.metadata.get('page', 'unknown')}]\n{doc.page_content}"
            for i, doc in enumerate(docs)
        ]
    )

    chain = context_compression_prompt | llm | StrOutputParser()

    compressed = chain.invoke({
        "question": question,
        "documents": documents_text
    })

    return compressed


def generate_advanced_context_with_compression(question, llm, vector_store, num_queries=7):
    """개선된 Multi-Query RAG with Context Compression"""

    # 1. 여러 변형 질문 생성
    generated_queries = generate_multiple_queries(question, llm, num_queries)

    print(f"\n[생성된 {len(generated_queries)}개의 변형 질문들]")
    for i, q in enumerate(generated_queries, 1):
        print(f"{i}. {q}")

    # 2. 각 질문으로 검색 후 통합
    print(f"\n[Multi-Query 검색 실행]")
    all_docs = []
    for i, q in enumerate(generated_queries, 1):
        search_results = vector_store.similarity_search(q, k=3)  # 각 쿼리당 최대 3개 문서
        if search_results:
            all_docs.extend(search_results)
            print(f"질문 {i}: {len(search_results)}개 문서 검색됨")
    
    # 3. 중복 문서 제거
    unique_docs = []
    seen = set()
    for doc in all_docs:
        if doc.page_content not in seen:
            unique_docs.append(doc)
            seen.add(doc.page_content)
    print(f"총 {len(all_docs)}개 문서 검색, 중복 제거 후 {len(unique_docs)}개 고유 문서")

    # 4. Context Compression 적용
    if unique_docs:
        print("\n[Context Compression 실행 중...]")
        original_length = len(''.join([doc.page_content for doc in unique_docs]))
        compressed_context = compress_context(question, unique_docs, llm)
        compressed_length = len(compressed_context)

        compression_ratio = round((1 - compressed_length/original_length) * 100, 1) if original_length > 0 else 0
        print(f"압축 완료: {original_length} → {compressed_length} 문자 (압축률: {compression_ratio})")
        return compressed_context
    
    else:
        print("관련 문서를 찾을 수 없습니다.")
        return ''


# QA 프롬프트 정의
qa_prompt = PromptTemplate.from_template(
    """
    당신은 질문-답변(Question-Answering)을 수행하는 AI 어시스턴트입니다. 당신의 업무는 주어진 문맥(context)에서 주어진 질문(question)에 답하는 것입니다.
    검색된 다음 문맥(context)을 사용하여 질문(question)에 답하세요. 만약, 주어진 문맥(context)에서 답을 찾을 수 없다면, '주어진 정보에서 질문에 대한 정보를 
    찾을 수 없습니다' 라고 답하세요. 질문과 관련성이 높은 내용만 답변하고 추측한 내용을 생성하지 마세요. 기술적인 용어나 이름은 번역하지 안혹 그대로 사용해 주세요.

    # Question
    {question}

    # Context
    {context}

    # Answer:
    """
)

# Multi-query 프롬프트 정의   
multi_query_prompt = PromptTemplate.from_template(
    """
    주어진 사용자 질문의 다양한 버전을 생성하는 AI입니다. 사용자의 질문을 paraphrasing해서 질문의 의도와 의미가 동일한 새로운 질문 7개를 만들어냅니다.
    질문 속 핵심 단어는 유지하고 조사나 수식어와 같은 부가적인 표현을 paraphrasing 합니다.

    각 질문은 다음과 같은 다양한 표현 방식을 사용하세요.
    1. 정의를 묻는 형태
    2. 설명을 요청하는 형태
    3. 구체적인 내용을 묻는 형태
    4. 절차나 과정을 묻는 형태
    5. 특징이나 특성을 묻는 형태
    6. 목적이나 이유를 묻는 형태
    7. 다른 용어로 표현한 형태

    질문: {question}

    7가지 다양한 질문:
    """
)

# Context compression 프롬프트 정의
context_compression_prompt = PromptTemplate.from_template(
    """
    당신은 문서 요약 전문가입니다. 주어진 여러 문서들에서 질문과 관련된 핵심 정보만을 추출하여 간결하게 요약해주세요.

    중복된 내용은 제거하고, 질문에 답하는데 필요한 가장 중요한 정보들만 포함하세요.
    요약된 내용은 원본의 의미를 보존하면서도 불필요한 세부사항은 제거해야 합니다.

    질문: {question}

    문서들:
    {documents}

    압축된 컨텍스트:
    """
)

# 벡터 DB 로드 또는 생성
if os.path.exists(VECTOR_DB_PATH):
    print("기존 벡터 DB를 로드합니다.")
    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
        )
    vector_store = FAISS.load_local(
        VECTOR_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
else:
    print("새로운 벡터 DB를 생성합니다.")
    vector_store = create_vector_db()

# LLM 설정
llm = OllamaLLM(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)

# QA 체인 정의
qa_chain = qa_prompt | llm | StrOutputParser()

# Context Compression 체인 정의
compression_chain = context_compression_prompt | llm | StrOutputParser()

# Basic Retriever
basic_retriever = vector_store.as_retriever()

# 사용자 질문 입력 및 실행
question = input("질문을 입력하세요: ")

advanced_context = generate_advanced_context_with_compression(
    question=question,
    llm=llm,
    vector_store=vector_store,
    num_queries=7
)

if advanced_context:
    result = qa_chain.invoke({
        "question": question,
        "context": advanced_context
    })

    print("\n[최종 답변]")
    print(result)

else:
    print("주어진 정보에서 질문에 대한 정보를 찾을 수 없습니다.")

