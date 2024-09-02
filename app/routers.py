from fastapi import APIRouter, Depends
from .scraper import Scraper
from .storage.json_storage import JSONStorage
from .notifier.console_notifier import ConsoleNotifier
from .notifier.email_notifier import EmailNotifier
from .cache import Cache
from .storage.storage import StorageBase
from .storage.sql_storage import SQLStorage
from .notifier.notifier import NotifierBase
from .models import Product, ScrapedData

router = APIRouter()

def get_storage(strategy: str = "json") -> StorageBase:
    if strategy == "sql":
        return SQLStorage(db_name="scraped_data.db")
    return JSONStorage(filename="scraped_data.json")

def get_notifier(strategy: str = "console") -> NotifierBase:
    if strategy == "email":
        return EmailNotifier(
            smtp_server="smtp.example.com",
            smtp_port=587,
            username="email@example.com",
            password="password",
            recipient="recipient@example.com"
        )
    return ConsoleNotifier()

@router.post("/scrape/")
def scrape_data(pages: int = 1, proxy: str = None, 
                storage: StorageBase = Depends(get_storage),
                notifier: NotifierBase = Depends(get_notifier)):
    scraper = Scraper(base_url="https://dentalstall.com/shop", proxy=proxy)
    cache = Cache()

    scraped_data = scraper.scrape(pages=pages)
    validated_data = ScrapedData(products=scraped_data)  # Validation occurs here

    updated_count = 0
    for item in validated_data.products:
        if cache.cache_product(item.product_title, item.product_price):
            updated_count += 1

    if updated_count > 0:
        storage.update_data(validated_data.products)

    notifier.notify(f"Scraping completed. {updated_count} products updated in the database.")

    return {"status": "success", "updated_count": updated_count}

