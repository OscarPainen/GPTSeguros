from celery import shared_task

@shared_task
def scrape_website(url):
    print(f"Scraping website: {url}")
    