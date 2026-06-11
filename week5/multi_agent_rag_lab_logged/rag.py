"""
수업용 Simple RAG 모듈
- reference 문서를 chunk로 분할
- Ollama embedding으로 vector index 생성
- embedding 실패 시 keyword search로 fallback
- LangChain/MCP 없이 RAG 구조를 직접 확인하기 위한 최소 구현
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
try:
    import ollama
except ImportError:
    ollama = None

from config import REFERENCE_DIR, VECTOR_STORE_DIR, EMBED_MODEL, TOP_K
from logger import log_step, log_detail, log_result


@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str
    embedding: Optional[List[float]] = None


def read_text_files(reference_dir: Path = REFERENCE_DIR) -> List[Dict[str, str]]:
    log_step("RAG 문서 로드", f"reference_dir={reference_dir}")
    docs = []
    for path in sorted(reference_dir.glob("*.txt")):
        docs.append({"source": path.name, "text": path.read_text(encoding="utf-8")})
        log_detail(f"문서 로드: {path.name}")
    log_result("로드 문서 수", len(docs))
    return docs


def split_text(text: str, chunk_size: int = 650, overlap: int = 120) -> List[str]:
    """문서를 일정 길이로 분할한다. 교육용이므로 단순 character 기준 사용."""
    cleaned = re.sub(r"\n{3,}", "\n\n", text.strip())
    if len(cleaned) <= chunk_size:
        return [cleaned]

    chunks = []
    start = 0
    while start < len(cleaned):
        end = start + chunk_size
        chunks.append(cleaned[start:end].strip())
        start = max(end - overlap, end)
    return [c for c in chunks if c]


def embed_text(text: str) -> Optional[List[float]]:
    """Ollama embedding 호출. 실패하면 None 반환."""
    if ollama is None:
        return None
    try:
        response = ollama.embed(model=EMBED_MODEL, input=text)
        return response["embeddings"][0]
    except Exception:
        return None


def build_index() -> Dict[str, Any]:
    log_step("RAG 인덱스 생성 시작")
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    chunks: List[Chunk] = []

    for doc_idx, doc in enumerate(read_text_files()):
        for chunk_idx, chunk_text in enumerate(split_text(doc["text"])):
            chunk_id = f"DOC{doc_idx:02d}_CHUNK{chunk_idx:03d}"
            embedding = embed_text(chunk_text)
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    source=doc["source"],
                    text=chunk_text,
                    embedding=embedding,
                )
            )
            status = "embedding ok" if embedding is not None else "embedding fallback 예정"
            log_detail(f"chunk 생성: {chunk_id} / source={doc['source']} / {status}")

    index = {
        "embedding_model": EMBED_MODEL,
        "chunks": [asdict(c) for c in chunks],
    }
    index_path = VECTOR_STORE_DIR / "rag_index.json"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    log_result("저장 경로", index_path)
    log_result("chunk 수", len(chunks))
    return index


def load_index() -> Dict[str, Any]:
    index_path = VECTOR_STORE_DIR / "rag_index.json"
    if not index_path.exists():
        log_detail("RAG 인덱스 파일이 없어 새로 생성합니다.")
        return build_index()
    log_detail(f"RAG 인덱스 로드: {index_path}")
    return json.loads(index_path.read_text(encoding="utf-8"))


def cosine_similarity(a: List[float], b: List[float]) -> float:
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)


def keyword_score(query: str, text: str) -> float:
    query_terms = [t for t in re.split(r"\W+", query.lower()) if len(t) >= 2]
    if not query_terms:
        return 0.0
    text_lower = text.lower()
    hits = sum(1 for term in query_terms if term in text_lower)
    return hits / math.sqrt(len(query_terms))


def search(query: str, top_k: int = TOP_K) -> Dict[str, Any]:
    """표준 evidence packet을 반환한다."""
    log_step("RAG 검색 시작", f"query={query}")
    index = load_index()
    chunks = index.get("chunks", [])
    query_embedding = embed_text(query)

    scored = []
    mode = "vector" if query_embedding is not None else "keyword"
    log_result("검색 모드", mode)

    for chunk in chunks:
        if mode == "vector" and chunk.get("embedding") is not None:
            score = cosine_similarity(query_embedding, chunk["embedding"])
        else:
            score = keyword_score(query, chunk["text"])
            mode = "keyword"
        scored.append({**chunk, "score": score})

    results = sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]
    results = [r for r in results if r["score"] > 0]
    log_result("검색 결과 수", len(results))

    context_blocks = []
    sources = []
    for i, r in enumerate(results, start=1):
        sources.append({"source": r["source"], "chunk_id": r["chunk_id"], "score": round(r["score"], 4)})
        log_detail(f"근거 {i}: {r['source']} / {r['chunk_id']} / score={round(r['score'], 4)}")
        context_blocks.append(f"[근거 {i}] source={r['source']} / chunk={r['chunk_id']}\n{r['text']}")

    return {
        "status": "ok" if results else "no_context",
        "mode": mode,
        "has_context": bool(results),
        "query": query,
        "context": "\n\n".join(context_blocks),
        "sources": sources,
        "results": results,
    }


def format_evidence_context(evidence_packet: Dict[str, Any]) -> str:
    if not evidence_packet.get("has_context"):
        return "[검색 근거 없음]\n제공된 reference 문서에서 관련 근거를 찾지 못했습니다."
    return "[검색 근거]\n" + evidence_packet["context"]
