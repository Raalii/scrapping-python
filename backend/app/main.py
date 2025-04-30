from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
from fastapi.middleware.cors import CORSMiddleware
from .scraper import scrape
from .pipeline import clean_text, detect_lang
from .vector_store import store_article, search_articles
from .llm import summarize, extract_keywords

app = FastAPI(title="News Summarizer API")

# Ajout du middleware CORS pour autoriser toutes les origines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes
    allow_headers=["*"],  # Autorise tous les headers
)



class UrlPayload(BaseModel):
    url: str

class QueryPayload(BaseModel):
    query: str

@app.post("/summarize")
async def summarize_endpoint(payload: UrlPayload):
    # 1. Scrape
    article = await scrape(payload.url)
    if not article.text:
        raise HTTPException(status_code=400, detail="Article vide ou inaccessible.")
    # 2. Clean
    text = clean_text(article.text)
    lang = detect_lang(text)
    # 3. Store
    article_id = str(uuid.uuid4())
    store_article(article_id, text)
    # 4. LLM Summary & keywords
    summary = summarize(text[:8000], lang)
    keywords = extract_keywords(text)
    return {
        "id": article_id,
        "lang": lang,
        "summary": summary,
        "keywords": keywords
    }

@app.post("/search")
def search_endpoint(payload: QueryPayload):
    return search_articles(payload.query)
