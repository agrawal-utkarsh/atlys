from bs4 import BeautifulSoup
import requests
from .models import Product, ScrapedData
from typing import List
from tenacity import retry, wait_fixed, stop_after_attempt
import traceback
import re

from typing import List
from bs4 import BeautifulSoup
import requests
from .models import Product
from tenacity import retry, wait_fixed, stop_after_attempt, retry_if_exception_type
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Scraper:


    def __init__(self, base_url: str, proxy: str = None):
        self.base_url = base_url
        self.proxy = proxy
        self.session = requests.Session()
        if proxy:
            self.session.proxies = {"http": proxy, "https": proxy}

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3), retry=retry_if_exception_type(requests.exceptions.RequestException))
    def scrape(self, pages: int = 1) -> List[Product]:
        products = []
        for page in range(1, pages + 1):
            url = f"{self.base_url}/page/{page}/"
            try:
                response = self._get_page(url)
                soup = BeautifulSoup(response.content, "html.parser")
                page_products = self._parse_products(soup)
                products.extend(page_products)
            except Exception as e:
                logger.error(f"Error scraping page {page}: {e}")
                logger.error(traceback.format_exc())
        return products

    @retry(wait=wait_fixed(2), stop=stop_after_attempt(3), retry=retry_if_exception_type(requests.exceptions.RequestException))
    def _get_page(self, url: str):
        logger.info(f"Fetching {url}")
        response = self.session.get(url)
        response.raise_for_status()
        return response

    def _parse_products(self, soup: BeautifulSoup) -> List[Product]:
        products = []
        
        # Select the list items containing the products
        product_elements = soup.select('ul.products > li.product')
        
        if not product_elements:
            logger.warning("No products found on page")
        
        for product_html in product_elements:
            try:
                # Extract the product title
                title_tag = product_html.select_one('.woo-loop-product__title a')
                title = title_tag.get_text(strip=True) if title_tag else 'No title'
                
                # Extract the product price
                price_tag = product_html.select_one('.mf-product-price-box .price')
                if price_tag:
                    price_str = price_tag.get_text(strip=True)
                    # Extracting numeric price (handling both simple and discounted prices)
                    price_match = re.search(r'₹(\d+(\.\d+)?)', price_str)
                    price = float(price_match.group(1)) if price_match else 0.0
                else:
                    price = 0.0
                
                # Extract the image URL
                img_tag = product_html.select_one('.mf-product-thumbnail img')
                image_url = img_tag['data-lazy-src'] if img_tag and 'data-lazy-src' in img_tag.attrs else 'No image URL'
                
                # Ensure image_url is a string
                image_url = str(image_url)
                
                # Create the Product object
                product = Product(
                    product_title=title,
                    product_price=price,
                    image_url=image_url
                )
                products.append(product)
            except Exception as e:
                logger.error(f"Error parsing product: {e}")
                logger.error(traceback.format_exc())
        
        return products