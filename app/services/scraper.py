import requests
from bs4 import BeautifulSoup

from app.models.schemas import CEORequest
from app.services.writer import write_to_csv
from app.utils.language import is_english

def scrape_article(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        text = " ".join(p.get_text() for p in soup.find_all("p"))
        return text.strip()
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"


import requests
from bs4 import BeautifulSoup
from app.services.serpapi_service import get_google_results
from app.services.cleaner import clean_text, clean_transcript
from app.services.relevance import estimate_relevance, get_relevance
from app.utils.export import export_to_csv, export_to_stata

YEARS = list(range(2014, 2023))

def get_standardized_source(url: str) -> str:
    family_map = {
        'fox': 'Fox News',
        'cnn': 'CNN',
        'nbc': 'NBC News',
        'cbs': 'CBS News',
        'wsj': 'Wall Street Journal',
        'dailycaller': 'Daily Caller',
        'americanthinker': 'American Thinker',
    }
    for key, val in family_map.items():
        if key in url:
            return val
    return "Unknown"

def scrape_article(url: str) -> str:
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.content, "html.parser")
        text = ' '.join([p.get_text() for p in soup.find_all("p")])
        return text
    except Exception as e:
        print(f"[ERROR] Failed scraping: {url} | {e}")
        return ""

def scrape_for_ceo(ceo: str, nicknames: list[str], company: str) -> list:
    aliases = nicknames + [ceo]
    all_records = []

    for year in YEARS:
        quoted_aliases = ' OR '.join([f'"{alias}"' for alias in aliases])
        query = f"site:foxnews.com OR site:foxbusiness.com {quoted_aliases}"
        print(f"[SERPAPI] Searching: {query} | Year: {year}")
        links = get_google_results(query, year)

        if not links:
            all_records.append({
                "ceo_year": f"{ceo} - {year}",
                "pub_date": "",
                "media_outlet_url": "",
                "transcript": "no data found",
                "standardized_source": "",
                "relevance_pct": 0
            })
            continue

        for link in links:
            url = link.get("link")
            snippet = link.get("snippet", "")
            pub_date = link.get("date", "")

            article_text = scrape_article(url)
            cleaned_text = clean_transcript(article_text)
            relevance = estimate_relevance(cleaned_text, aliases, company)
            source = get_standardized_source(url)

            all_records.append({
                "ceo_year": f"{ceo} - {year}",
                "pub_date": pub_date,
                "media_outlet_url": url,
                "transcript": cleaned_text,
                "standardized_source": source,
                "relevance_pct": relevance
            })

    export_to_csv(all_records)
    export_to_stata(all_records)
    return all_records



def scrape_ceo_articles(request: CEORequest):
    ceo = request.ceo_name
    aliases = request.nicknames + [ceo]
    output = []

    for year in YEARS:
        query = (
            f"site:foxnews.com OR site:foxbusiness.com \"{ceo}\" OR " +
            " OR ".join(f'"{alias}"' for alias in aliases)
        )


        results = get_google_results(query, year)
        
        print(f"Year {year} | Query: {query} | Results: {len(results)}")

        if not results:
            output.append({
                "ceo_year": f"{ceo} - {year}",
                "pub_date": "",
                "media_outlet_url": "",
                "transcript": "no data found",
                "standardized_source": "",
                "relevance_pct": 0
            })
            continue

        for r in results:
            url = r.get("link")
            pub_date = r.get("snippet", "").split("·")[0].strip()
            raw_text = scrape_article(url)
            if not raw_text or not is_english(raw_text):
                continue

            cleaned = clean_text(raw_text)
            relevance = get_relevance(cleaned, aliases)
            source = get_standardized_source(url)

            output.append({
                "ceo_year": f"{ceo} - {year}",
                "pub_date": pub_date,
                "media_outlet_url": url,
                "transcript": cleaned,
                "standardized_source": source,
                "relevance_pct": relevance
            })

    write_to_csv(output)
    return {"message": "Scraping completed.", "records": len(output)}

