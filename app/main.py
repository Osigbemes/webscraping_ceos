from fastapi import FastAPI
from app.models.schemas import CEORequest
from app.services.serpapi_service import get_google_results
from app.services.scraper import scrape_article
from app.services.cleaner import clean_text, get_standardized_source
from app.services.relevance import get_relevance
from app.utils.language import is_english
from app.services.writer import write_to_csv
from app.config import YEARS
from app.routes import scrape

app = FastAPI()
app.include_router(scrape.router)
