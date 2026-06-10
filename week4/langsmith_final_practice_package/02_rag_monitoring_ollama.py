import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

MODEL_NAME = os.getenv("OLLAMA_MODEL", "exaone3.5")
EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

DATA_PATH = Path("sample_quality_report.txt")
DB_DIR = "chroma_langsmith_demo"

def build_retriever():
    text = DATA_PATH.read_text(encoding="utf-8")
    docs = [Document(page_content=text, metadata={"source": str(DATA_PATH)})]

    splitter = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=80)
    chunks = splitter.split_documents(docs)

    embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_BASE_URL)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR,
        collection_name="quality_report_demo",
    )
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def format_docs(docs: list[Document]) -> str:
    return "\n\n".join(doc.page_content for doc in docs)

def build_chain():
    retriever = build_retriever()

    prompt = PromptTemplate.from_template(
        '''
당신은 제조 품질 리포트 분석 도우미입니다.
아래 문서 내용에 근거해서만 답변하세요.
문서에서 확인할 수 없는 내용은 추측하지 말고, "문서에서 확인할 수 없습니다."라고 답변하세요.

[문서 내용]
{context}

[질문]
{question}

[답변]
'''.strip()
    )

    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=0)

    return (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

if __name__ == "__main__":
    chain = build_chain()
    print("RAG 질문을 입력하세요. 종료하려면 exit")

    while True:
        q = input("\n질문: ").strip()
        if q.lower() in ["exit", "quit", "q"]:
            break
        result = chain.invoke(q)
        print("\n답변:")
        print(result)
        print("\nLangSmith Runs에서 RunnableSequence와 VectorStoreRetriever를 확인하세요.")
