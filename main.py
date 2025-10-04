import asyncio
import logging

from common.logger_config import setup_logging
from scrapers.test import test_logging

logger = logging.getLogger(__name__)


async def main():
    setup_logging()
    logger.info("Starting LightBulbFlow application")
    test_logging()
    pass


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("LightBulbFlow stopped by keyboard interrupt")
