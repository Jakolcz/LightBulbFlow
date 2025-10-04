import os
import logging.config
import yaml
from pathlib import Path


def setup_logging(
        config_path="config/logging.yaml",
        default_level=logging.INFO,
        env_key="LOG_CFG"
):
    """
    Setup logging configuration from a YAML file
    """
    path = os.getenv(env_key, config_path)

    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                # Ensure logs directory exists
                Path("logs").mkdir(exist_ok=True)
                logging.config.dictConfig(config)
            except Exception as e:
                print(f"Error in logging configuration: {e}")
                print("Using default configs")
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print(f"Config file {path} not found. Using default configs")
