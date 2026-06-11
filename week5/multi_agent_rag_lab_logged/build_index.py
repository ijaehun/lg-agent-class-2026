from rag import build_index

if __name__ == "__main__":
    index = build_index()
    print(f"RAG index 생성 완료: {len(index['chunks'])} chunks")
