import logging
import os

logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
    level=getattr(logging, os.environ.get("LOGLEVEL", "INFO").upper()),
)
