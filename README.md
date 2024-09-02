# Scraping Tool using FastAPI

## Overview

This project is a web scraping tool built with FastAPI. The tool is designed to scrape product data (name, price, and image) from a target website and store it in a local JSON file. It also includes features like authentication, caching, and notifications.

## Features

- **Scraping**: Extracts product information from a specified number of pages.
- **Storage**: Stores scraped data in a local JSON file.
- **Caching**: Uses Redis to cache product prices and avoid unnecessary updates.
- **Authentication**: Secures the API endpoint with a static token.
- **Notifications**: Prints the result of the scraping process to the console.

## Running
### Start server
    uvicorn app.main:app --reload
<br>
<br>

### Curl request
    curl -X \
    POST "http://127.0.0.1:8000/scrape/" -H \
    "x-token: dummy-token" -d '{"pages": 5, "notifier_strategy": "logger"}'
