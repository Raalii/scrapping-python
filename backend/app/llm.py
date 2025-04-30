import os, openai
from typing import List

openai.api_key = os.getenv("OPENAI_API_KEY")

EMB_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"

def embed(text: str) -> List[float]:
    res = openai.Embedding.create(model=EMB_MODEL, input=text)
    return res.data[0].embedding

def summarize(text: str, lang: str) -> str:
    prompt = f"Langue: {lang}. Résume l'article suivant en 200 mots maximum et propose 5 mots-clés à la fin.\n\n{text}"
    resp = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()

def extract_keywords(text: str) -> List[str]:
    prompt = f"Donne uniquement une liste JSON de 5 mots-clés saisis en minuscules sans explication, pour le texte suivant:\n\n{text}"
    resp = openai.ChatCompletion.create(
        model=CHAT_MODEL,
        messages=[{"role":"user","content":prompt}],
        temperature=0.2,
    )
    try:
        return eval(resp.choices[0].message.content.strip())
    except Exception:
        return []
