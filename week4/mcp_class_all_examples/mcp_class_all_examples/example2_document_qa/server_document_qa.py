# example2_document_qa/server_document_qa.py
# MCP 예제2: 문서 Q&A 서버
#
# Ollama가 실행 중이면 로컬 LLM으로 답변합니다.
# Ollama가 없으면 검색된 문장 기반의 간단 답변을 생성합니다.

from pathlib import Path
import os
import re
from typing import Any

import chromadb
import fitz
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP
from sentence_transformers import SentenceTransformer


load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "exaone3.5")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

DB_DIR = Path("example2_document_qa/chroma_db")
COLLECTION_NAME = "quality_documents"

mcp = FastMCP(
    "DocumentQAServer",
    instructions="PDF/TXT 문서를 업로드하고, 문서 내용을 기반으로 질문에 답하는 MCP 서버입니다.",
)

print("임베딩 모델 로딩 중입니다. 처음 실행 시 시간이 걸릴 수 있습니다.")
embedding_model = SentenceTransformer(EMBED_MODEL)

chroma_client = chromadb.PersistentClient(path=str(DB_DIR))
collection = chroma_client.get_or_create_collection(COLLECTION_NAME)


def read_pdf_text(file_path: str) -> str:
    """PDF 파일에서 텍스트를 추출합니다."""
    doc = fitz.open(file_path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    doc.close()
    return "\n".join(texts)


def read_text_file(file_path: str) -> str:
    """TXT 파일을 읽습니다."""
    return Path(file_path).read_text(encoding="utf-8")


def load_document_text(file_path: str) -> str:
    """PDF 또는 TXT 문서를 읽습니다."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")

    ext = path.suffix.lower()

    if ext == ".pdf":
        return read_pdf_text(str(path))

    if ext == ".txt":
        return read_text_file(str(path))

    raise ValueError("지원하는 파일 형식은 PDF와 TXT입니다.")


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 80) -> list[str]:
    """문서를 작은 조각으로 나눕니다."""
    clean = "\n".join(line.strip() for line in text.splitlines() if line.strip())

    if not clean:
        return []

    chunks = []
    start = 0

    while start < len(clean):
        end = start + chunk_size
        chunks.append(clean[start:end])
        start = end - overlap

        if start < 0:
            start = 0
        if start >= len(clean):
            break

    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    """텍스트를 임베딩 벡터로 변환합니다."""
    vectors = embedding_model.encode(texts, normalize_embeddings=True)
    return vectors.tolist()


def ollama_is_available() -> bool:
    """Ollama 서버가 실행 중인지 확인합니다."""
    try:
        response = requests.get(OLLAMA_URL.replace("/api/generate", "/api/tags"), timeout=2)
        return response.status_code == 200
    except Exception:
        return False


def call_ollama(prompt: str) -> str:
    """Ollama 로컬 LLM을 호출합니다."""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=120)
    response.raise_for_status()
    return response.json().get("response", "").strip()


def fallback_answer(query: str, documents: list[str]) -> str:
    """Ollama가 없을 때 검색된 문장을 바탕으로 간단히 답합니다."""
    context = "\n".join(documents)
    sentences = re.split(r"(?<=[.!?。])\s+|(?<=다\.)\s*", context)
    keywords = [word for word in re.findall(r"[가-힣A-Za-z0-9]+", query) if len(word) >= 2]

    selected = []
    for sentence in sentences:
        if any(keyword in sentence for keyword in keywords):
            selected.append(sentence.strip())

    if not selected:
        selected = documents[:2]

    return " ".join(selected[:3])[:700]


@mcp.tool
def upload_document(file_path: str) -> dict[str, Any]:
    """
    PDF/TXT 문서를 읽고, chunk 단위로 임베딩하여 ChromaDB에 저장합니다.

    Args:
        file_path: 업로드할 문서 경로
    """
    try:
        path = Path(file_path)
        text = load_document_text(str(path))
        chunks = chunk_text(text)

        if not chunks:
            return {
                "status": "error",
                "message": "문서에서 텍스트를 추출하지 못했습니다.",
            }

        embeddings = embed_texts(chunks)
        ids = [f"{path.name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [
            {
                "source": str(path),
                "file_name": path.name,
                "chunk_index": i,
            }
            for i in range(len(chunks))
        ]

        collection.upsert(
            ids=ids,
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return {
            "status": "success",
            "message": "문서가 벡터 DB에 저장되었습니다.",
            "file_name": path.name,
            "num_chunks": len(chunks),
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


@mcp.tool
def ask_question(query: str, top_k: int = 3) -> dict[str, Any]:
    """
    업로드된 문서에서 관련 내용을 검색하고 답변합니다.

    Args:
        query: 사용자 질문
        top_k: 검색할 문서 조각 수
    """
    try:
        query_embedding = embed_texts([query])[0]

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            return {
                "status": "error",
                "message": "검색된 문서가 없습니다. 먼저 upload_document를 실행하세요.",
            }

        context = "\n\n".join([f"[문서 조각 {i+1}]\n{doc}" for i, doc in enumerate(documents)])

        if ollama_is_available():
            prompt = f"""
당신은 품질 리포트 분석 도우미입니다.
아래 문서 내용에 근거해서만 답변하세요.
문서에서 확인할 수 없는 내용은 추측하지 마세요.

[문서 내용]
{context}

[질문]
{query}

[답변 조건]
- 한국어로 답변하세요.
- 핵심만 3~5문장으로 답변하세요.
- 근거가 되는 내용을 함께 설명하세요.

[답변]
""".strip()
            answer = call_ollama(prompt)
            answer_type = "ollama_local_llm"
        else:
            answer = fallback_answer(query, documents)
            answer_type = "fallback_search_based_answer"

        sources = []
        for i, metadata in enumerate(metadatas):
            sources.append({
                "rank": i + 1,
                "file_name": metadata.get("file_name"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distances[i] if i < len(distances) else None,
            })

        return {
            "status": "success",
            "answer_type": answer_type,
            "query": query,
            "answer": answer,
            "sources": sources,
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


if __name__ == "__main__":
    print("Document QA MCP Server 실행 중")
    print("접속 주소: http://127.0.0.1:8002/mcp")
    print("종료하려면 Ctrl + C")
    mcp.run(transport="http", host="127.0.0.1", port=8002)
