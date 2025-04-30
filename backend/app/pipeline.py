import re, unicodedata, langdetect

def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def detect_lang(text: str) -> str:
    try:
        return langdetect.detect(text)
    except langdetect.lang_detect_exception.LangDetectException:
        return "unknown"
