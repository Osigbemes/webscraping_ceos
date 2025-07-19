from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def get_google_results(query, year):
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "q": query,
        "num": 20,
        "tbs": f"cdr:1,cd_min:1/1/{year},cd_max:12/31/{year}"
    }

    print(f"[SERPAPI] Searching: {params['q']} | Year: {year}")
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict().get("organic_results", [])
        return results
    except Exception as e:
        print(f"[ERROR] SerpAPI error: {e}")
        return []
