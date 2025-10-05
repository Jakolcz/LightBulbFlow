import logging

from config.models import RedditConfig
from scrapers.ScraperProtocol import ScraperProtocol

logger = logging.getLogger(__name__)


class RedditScraper(ScraperProtocol):
    def __init__(self, config: RedditConfig):
        self.config = config
        pass

    def scrape(self):
        # Placeholder for scraping logic
        logger.info(f"Scraping Reddit with config: {self.config}")
