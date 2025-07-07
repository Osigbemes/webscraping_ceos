from fastapi import APIRouter
from app.models.schemas import CEORequest
from app.services.scraper import scrape_ceo_articles, scrape_for_ceo

router = APIRouter()

@router.post("/scrape/")
def scrape_ceos(request: CEORequest):
    records = scrape_for_ceo(request.ceo_name, request.nicknames, request.company)
    return {"message": "Scraping completed.", "records": len(records)}

@router.post("/scrape_ceo_articles/")
def scrape_articles(request: CEORequest):
    """
    Endpoint to scrape articles related to a CEO.
    """
    records = scrape_ceo_articles(request)
    return records