from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
import bs4

section_splitter = "\n\n---\n\n"

"""
RAG 실습 코드 (Web Page RAG)

- 웹 페이지 문서 로드
  -> HTML에서 필요한 본문 영역 추출
  -> 문서 분할
  -> 임베딩
  -> FAISS 벡터 저장소 구축
  -> 사용자 질문 정의
  -> 벡터 DB에서 관련 문서 검색
  -> 검색된 문서를 context로 구성
  -> context와 질문을 프롬프트에 입력
  -> LLM을 이용한 답변 생성

- 주요 구성
    1. 웹 문서 로딩
        - WebBaseLoader로 지정한 URL의 HTML 문서를 로드
        - BeautifulSoup의 SoupStrainer를 사용하여 기사 본문 영역만 선택적으로 추출
        - 웹 페이지 구조가 변경되면 class selector를 수정해야 할 수 있음

    2. 문서 분할
        - RecursiveCharacterTextSplitter로 긴 웹 문서를 작은 chunk로 분할
        - chunk_size와 chunk_overlap을 조정하여 검색 단위를 설정
        - chunk 크기에 따라 검색 결과와 최종 답변이 달라질 수 있음

    3. 벡터 DB 생성
        - OllamaEmbeddings로 각 chunk를 embedding vector로 변환
        - FAISS에 embedding vector와 문서 chunk를 저장
        - 이 예제에서는 메모리상 vector_store를 생성하며, 로컬 저장은 수행하지 않음

    4. Retriever 검색
        - 사용자 질문을 기준으로 FAISS 벡터 DB에서 관련 chunk 검색
        - 검색된 chunk들을 하나의 context로 결합

    5. RAG 답변 생성
        - 검색된 context와 사용자 질문을 ChatPromptTemplate에 입력
        - OllamaLLM을 사용하여 웹 문서 기반 답변 생성

- 사전 작업
    - Ollama embedding 모델 설치
        ollama pull nomic-embed-text

    - Ollama 생성 모델 설치
        ollama pull llama3.1

    - Python package 설치
        pip install beautifulsoup4
        pip install langchain-community
        pip install faiss-cpu
        pip install langchain-ollama
        pip install langchain-text-splitters

- 실행 전 확인 사항
    - 인터넷 연결이 필요함
    - 대상 웹 페이지에 접근 가능해야 함
    - Ollama 서버가 실행 중이어야 함
    - EMBEDDING_MODEL은 임베딩 전용 모델을 사용해야 함
        예: nomic-embed-text
    - LLM_MODEL은 generate를 지원하는 생성 모델을 사용해야 함
        예: llama3.1
    - WebBaseLoader의 bs_kwargs selector는 웹 페이지 구조에 따라 수정될 수 있음

- 참고
    - 이 예제는 웹 페이지 전체가 아니라 특정 HTML 영역만 추출함
    - 웹 사이트 구조가 바뀌면 문서 로딩 결과가 비어 있을 수 있음
    - chunk_size와 chunk_overlap을 바꾸면 검색되는 문서와 답변이 달라질 수 있음
"""

OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.1"

# 1. 웹 페이지에서 문서를 로드하기 위한 WebBaseLoader 설정
loader = WebBaseLoader(
    web_paths=("https://www.bbc.com/korean/articles/cl4yml4l6j1o",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            "div",
            attrs={"class":["css-1k9op6x e17x9cvu0"]}, # BBC 뉴스 웹 페이지에서 기사 본문이 포함된 div 요소를 선택하기 위한 클래스 이름입니다. 실제 웹 페이지 구조에 따라 이 값을 조정해야 할 수 있습니다.
        )
    ),
)

docs = loader.load()
print(f"문서의 수: {len(docs)}")
print(f"첫 번째 문서 출력")
print(docs[0])  # 첫 번째 문서의 내용을 출력
print(section_splitter)  # 구분자 출력

# 2. 문서 분할 (Splitting)
# 문서가 너무 길면 모델이 처리하기 어려울 수 있으므로, RecursiveCharacterTextSplitter를 사용하여 문서를 chunk size로 분할합니다.
# chunk_size=500 -> 각 텍스트 조각의 최대 길이를 500자로 설정, chunk_overlap=100 -> 각 텍스트 조각이 100자씩 겹치도록 설정하여 문맥 유지.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
print(f"분할된 텍스트 조각의 수: {len(splits)}")
print(section_splitter)  # 구분자 출력

# 3. 임베딩 (Embedding)
# Ollama 임베딩 모델을 사용하여 텍스트 조각을 벡터로 변환합니다.
# model="nomic-embed-text"은 Ollama에서 사용할 임베딩 모델을 지정하는 부분입니다. 실제로 사용 가능한 모델 이름은 Ollama의 문서를 참조하여 확인해야 합니다. (ex. "nomic-embed-text" 대신 "exaone3.5:7.8b" 등)
embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)

# 4. 벡터 저장소 구축
# 문서를 임베딩한 후 FAISS 벡터 저장소를 구축하여 벡터 저장
vector_store = FAISS.from_documents(documents=splits, embedding=embeddings)

# 4-1. 쿼리 저장소 검색을 위한 retriever 생성
retriever = vector_store.as_retriever()

# 5. 쿼리 처리 (Query-Retriever): 벡터 저장소에서 관련 문서를 검색
# 사용자의 질문을 정의합니다.
question = "이 기사의 주요 내용은 무엇인가요?"
# 설정된 질문을 임베딩하여 벡터로 변환
# 변환한 질문 벡터를 이용하여 FAISS 벡터 저장소에서 유사한 벡터를 검색하여 관련 문서를 반환
retrieved_docs = retriever.invoke(question)
print(f"검색된 문서의 수: {len(retrieved_docs)}")
for i, doc in enumerate(retrieved_docs):
    print(f"문서 {i+1} 내용:")
    print(doc.page_content)  # 검색된 문서의 내용을 출력
combined_docs = "\n\n".join([doc.page_content for doc in retrieved_docs])
print(section_splitter)  # 구분자 출력
print("검색된 문서의 통합본 내용:")
print(combined_docs)  # 검색된 문서의 내용을 출력
print(section_splitter)  # 구분자 출력

# 6. 검색된 문서를 첨부해서 PROMPT 생성
# 검색된 문서를 합쳐서 컨텍스트 문자열을 만들고 사용자 질문 준비
formatted_prompt = {"context": combined_docs, "question": question}

# LLM 모델 초기화 및 프롬프트 템플릿 정의
llm = OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_BASE_URL)
prompt = ChatPromptTemplate.from_template(
    """다음 컨텍스트를 기반으로 질문에 답변해주세요.

컨텍스트:
{context}

질문: {question}

답변:"""
)
print("생성된 프롬프트:")
print(prompt.format(**formatted_prompt))
print(section_splitter)  # 구분자 출력

# RAG 체인 구성
chain = (
    {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 7. LLM을 이용한 답변 생성
print("LLM이 생성한 답변:")
for chunk in chain.stream(formatted_prompt):
    print(chunk, end="", flush=True)


# TODO
# - chunk size, chunk overlap 조정해보며 검색되는 문서가 달라지는 양상과, 같은 질문에 대해 답변이 달라지는 양상 관찰하기