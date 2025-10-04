import asyncio
import logging

from src.common.logger_config import setup_logging

logger = logging.getLogger(__name__)


async def main():
    setup_logging()
    logger.info("Starting LightBulbFlow application")
    pass


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("LightBulbFlow stopped by keyboard interrupt")
