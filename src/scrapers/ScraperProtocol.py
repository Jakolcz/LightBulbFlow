from typing import Protocol


class ScraperProtocol(Protocol):
    """Protocol defining the interface for all scrapers."""

    def scrape(self) -> None:
        """Perform the scraping operation."""
        ...
