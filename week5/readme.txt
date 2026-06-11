pip install -r requirements.txt
ollama pull llama3.1:8b
ollama pull nomic-embed-text
python build_index.py
python chat_cli.py
