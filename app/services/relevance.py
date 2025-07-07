import spacy
nlp = spacy.load("en_core_web_sm")

def get_relevance(text, aliases):
    doc = nlp(text)
    relevant = [sent for sent in doc.sents if any(alias.lower() in sent.text.lower() for alias in aliases)]
    total_words = len(text.split())
    relevant_words = len(" ".join(str(s) for s in relevant).split())
    return round((relevant_words / total_words) * 100, 2) if total_words else 0

def estimate_relevance(text: str, aliases: list[str], company: str) -> float:
    doc = nlp(text)
    match_count = 0

    for token in doc:
        if token.text.lower() in [a.lower() for a in aliases]:
            match_count += 1

    # Extra: boost relevance if company is mentioned
    if company.lower() in text.lower():
        match_count += 3  # small bonus weight

    relevance_ratio = match_count / (len(doc) or 1)
    return round(min(relevance_ratio * 100, 100), 2)
