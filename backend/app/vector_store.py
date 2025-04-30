import os
import chromadb
from .llm import embed

client = chromadb.PersistentClient(path=os.getenv("CHROMA_PATH", "/tmp/chroma"))
collection = client.get_or_create_collection("articles")

def store_article(article_id: str, text: str):
    vec = embed(text)
    collection.add(ids=[article_id], documents=[text], embeddings=[vec])

def search_articles(query: str, k: int = 5):
    vec = embed(query)
    res = collection.query(query_embeddings=[vec], n_results=k)
    return res
