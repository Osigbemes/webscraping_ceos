from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def get_google_results(query, year):
    params = {
        "api_key": "5dc29846d1c25d11ceabe8c02a373e54992c61299d28a4fadc052220ca9dcbb8",
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
    
    # search = GoogleSearch(params)
    # response = search.get_dict()

    # # log if something goes wrong
    # if "error" in response:
    #     print(f"[ERROR] SerpAPI error: {response['error']}")
    #     return []

    # results = response.get("organic_results", [])
    # print(f"[INFO] Found {len(results)} results")
    # return results
