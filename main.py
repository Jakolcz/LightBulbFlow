import asyncio
import logging
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from common.logger_config import setup_logging

logger = logging.getLogger(__name__)


def parse_arguments():
    import argparse

    parser = argparse.ArgumentParser(description="LightBulbFlow Application")
    parser.add_argument('-c', '--config', type=str, default='config.yaml', help='Path to the configuration file')
    return parser.parse_args()


async def main():
    setup_logging()
    parse_arguments()
    logger.info("Starting LightBulbFlow application")
    pass


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("LightBulbFlow stopped by keyboard interrupt")
