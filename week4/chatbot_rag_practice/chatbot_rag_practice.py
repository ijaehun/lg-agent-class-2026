import os, glob
import re
import shutil
from typing import List, Dict
import time
import fitz
import streamlit as st

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import Runnable


"""
RAG 실습 코드 (RAG 예제 4)
- 여러 PDF 문서 로드 -> 문서 분할 -> 임베딩 -> 벡터 저장소 구축 -> 쿼리 처리 -> 검색된 문서를 첨부해서 프롬프트 생성 -> LLM을 이용한 답변 생성 (RAG 체인 구성)
- 사전 작업
    - Ollama embedding을 위하여 다음 명령어로 embedding 모델 Ollama에 추가
        ollama pull nomic-embed-text
    - 다음 package 설치
        pip install PyMuPDF
        pip install langchain-community
        pip install faiss-cpu
        pip install langchain-ollama
        pip install langchain-text-splitters
        pip install streamlit
        pip install typing

- 실행 코드
    streamlit run rag_practice.py

"""

VECTOR_DB_PATH = "./vector_db/faiss_vector_db"
DOCUMENT_PATH = "./documents"
IMAGE_OUTPUT_PATH = "./pdf_images"
OLLAMA_BASE_URL = "http://localhost:11434"
EMBEDDING_MODEL = "nomic-embed-text"
LLM_MODEL = "llama3.1" # (TODO) "daynice/kure-v1"로 바꿔서 실험해보기

###################################### 1단계: PDF 문서를 벡터 DB에 저장하는 함수 정의 ######################################

## 1. 임시 폴더에 파일 저장
# PDF 관련 각종 작업을 하기 위해 (Chunking, parsing, ...)
def save_uploadedfile(uploadedfile: UploadedFile):
    temp_dir = "./PDF_temp"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    file_path = os.path.join(temp_dir, uploadedfile.name)
    with open(file_path, "wb") as f:
        f.write(uploadedfile.read())
    return file_path

## 2. 지정된 PDF 파일을 document로 변환
# Page content, metadata 정보를 있음
def pdf_to_documents(pdf_path: str) -> List[Document]:
    documents = []
    loader = PyMuPDFLoader(pdf_path)
    doc = loader.load()
    for d in doc:
        d.metadata['file_path'] = pdf_path
    documents.extend(doc)
    return documents

## 3. Document를 더 작은 document로 변환
# 더 정교하게 문서를 원하는 형태로 저장하기 위해
def chunk_documents(documents: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    return text_splitter.split_documents(documents)

## 4. Document를 벡터DB로 저장
# FAISS DB 사용
@st.cache_resource(show_spinner=False)
def get_embeddings_model():
    return OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)

def save_to_vector_store(documents: List[Document], progress_bar=None, status_text=None) -> None:
    embeddings = get_embeddings_model()

    if progress_bar and status_text:
        status_text.text("임베딩 벡터 생성 중...")

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    vector_store.save_local(VECTOR_DB_PATH)
    
    if progress_bar and status_text:
        progress_bar.progress(100)
        status_text.text("벡터 DB 저장 완료")


###################################### 2단계: RAG 기능 구현 ######################################

## 사용자 질문에 대한 RAG 처리
# - 벡터 DB 호출
# - 질문과 유사한 문서 추출하는 Retriever 생성
# - RAG 체인 실행
def process_question(user_question):
    embeddings = get_embeddings_model()
    ## 벡터 DB 호출
    new_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    
    ## 관련 문서 3개를 호출하는 Retriever 생성
    retriever = new_db.as_retriever(search_kwargs={"k": 3})
    ## 사용자 질문을 기반으로 관련 문서 3개 검색
    retrieve_docs : List[Document] = retriever.invoke(user_question)

    ## RAG 체인 선언
    chain = get_rag_chain()
    ## 질문과 문맥을 넣어서 체인 결과 호출
    context = "\n\n".join([doc.page_content for doc in retrieve_docs])
    response = chain.invoke({
        "question": user_question,
        "context": context}
        )
    return response, retrieve_docs

def delete_existing_vector_db():
    if os.path.exists(VECTOR_DB_PATH):
        shutil.rmtree(VECTOR_DB_PATH)

# RAG 체인 정의
# - PromptTemplate 정의
# - 체인은 prompt -> model -> String Output 연결
@st.cache_resource
def get_model():
    return OllamaLLM(model=LLM_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)

def get_rag_chain() -> Runnable:
    template = """
    다음의 컨텍스트를 활용해서 질문에 대답해줘
    - 질문에 대한 응답을 해줘
    - 간결하게 5줄 이내로 해줘
    - 곧바로 응답결과를 말해줘
    컨텍스트: {context}
    질문: {question}
    """
    custom_rag_prompt = PromptTemplate.from_template(template)
    model = get_model()
    return custom_rag_prompt | model | StrOutputParser()


###################################### 3단계: 응답결과와 문서를 함께 보도록 도와주는 함수 ######################################

@st.cache_data(show_spinner=False)
# 각 페이지를 순회하며 PNG 형식으로 폴더에 페이지 이미지 저장
def convert_pdf_to_images(pdf_path: str, dpi: int = 250) -> List[str]:
    doc = fitz.open(pdf_path) # 문서 열기
    image_paths = []

    # 이미지 저장용 폴더 생성
    output_folder = IMAGE_OUTPUT_PATH
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_num in range(len(doc)): # 각 페이지를 순회
        page = doc.load_page(page_num) # 페이지 로드

        zoom = dpi / 72 # 72이 기본 DPI
        mat = fitz.Matrix(zoom, zoom) # 확대/축소 매트릭스 생성
        pix = page.get_pixmap(matrix=mat) # 페이지를 이미지로 변환, type: ignore

        image_path = os.path.join(output_folder, f"page_{page_num + 1}.png") # 페이지 이미지 저장 page_1.png, page_2.png, ...
        pix.save(image_path) # PNG 형태로 저장
        image_paths.append(image_path) # 경로를 저장

    return image_paths

# 파일에서 이미지 인식 후 화면에 렌더링
def display_pdf_page(image_path: str, page_number: int) -> None:
    image_bytes = open(image_path, "rb").read() # 파일에서 이미지 인식
    st.image(image_bytes, caption=f"Page {page_number}", output_format="PNG", width=600) # Streamlit을 이용해 이미지 출력

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]


def build_vector_db(uploaded_files):
    delete_existing_vector_db()
    st.cache_data.clear()

    if uploaded_files is None or len(uploaded_files) == 0:
        st.warning("PDF 파일을 먼저 업로드해주세요.")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()

    all_documents = []

    status_text.text("PDF 파일 저장 및 로딩 중...")

    for uploaded_file in uploaded_files:
        saved_path = save_uploadedfile(uploaded_file)
        documents = pdf_to_documents(saved_path)
        all_documents.extend(documents)

    progress_bar.progress(30)
    status_text.text(f"PDF 로딩 완료: 총 {len(all_documents)} 페이지")
    
    chunked_documents = chunk_documents(all_documents)

    progress_bar.progress(60)
    status_text.text(f"문서 분할 완료: 총 {len(chunked_documents)}개 chunk")

    save_to_vector_store(
        chunked_documents,
        progress_bar=progress_bar,
        status_text=status_text
    )

    st.success("벡터 DB 생성 완료")


###################################### 4단계: Streamlit 메인 실행부 ######################################

st.title("PDF RAG 검색 시스템")

st.write("PDF를 업로드한 뒤, 문서 내용에 대해 질문할 수 있습니다.")

uploaded_files = st.file_uploader(
    "PDF 파일 업로드",
    type=["pdf"],
    accept_multiple_files=True
)

if st.button("PDF 벡터 DB 생성"):
    build_vector_db(uploaded_files)

st.divider()

user_question = st.text_input("질문을 입력하세요.")

if st.button("질문하기"):
    if not user_question:
        st.warning("질문을 입력해주세요.")
    elif not os.path.exists(VECTOR_DB_PATH):
        st.warning("먼저 PDF 벡터 DB를 생성해주세요.")
    else:
        response, retrieve_docs = process_question(user_question)

        st.subheader("LLM 답변")
        st.write(response)

        st.subheader("검색된 관련 문서")

        for i, doc in enumerate(retrieve_docs):
            source_path = doc.metadata.get("file_path", "")
            page_number = doc.metadata.get("page", 0)

            with st.expander(f"검색 결과 {i+1} | Page {page_number+1}"):
                st.write(doc.page_content)

                if source_path:
                    image_paths = convert_pdf_to_images(source_path)

                    if page_number < len(image_paths):
                        display_pdf_page(
                            image_paths[page_number],
                            page_number+1
                        )


