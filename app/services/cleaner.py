import re
from app.config import MEDIA_FAMILY_MAP

def clean_text(text):
    text = re.sub(r'(Contributor|Published on|Font Size).*', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def get_standardized_source(url):
    for key, val in MEDIA_FAMILY_MAP.items():
        if key in url:
            return val
    return "Unknown"

def clean_transcript(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\b\w+\sContributor\b", "", text)
    text = re.sub(r"\b\d{1,2}:\d{2}\s?(AM|PM)?\s?(ET|PT|GMT)?\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Font Size:?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Published:[^\n]*Updated:[^\n]*\n", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()