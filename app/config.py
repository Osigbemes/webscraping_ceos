from decouple import config
import os
from dotenv import load_dotenv

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

MEDIA_FAMILY_MAP = {
    'fox': 'Fox News',
    'cnn': 'CNN',
    'nbc': 'NBC News',
    'cbs': 'CBS News',
    'wsj': 'Wall Street Journal',
    'dailycaller': 'Daily Caller',
    'americanthinker': 'American Thinker',
}
YEARS = list(range(2014, 2023))
