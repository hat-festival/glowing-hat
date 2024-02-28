from pathlib import Path

from redis import Redis

from lib.logger import logging


def all_entries(path):
    """Find all items in a dir."""
    return sorted(Path(path).glob("*"))


def populate():
    """Load the orderings into Redis."""
    redis = Redis()

    if not redis.exists("sorts:(1.0, 1.0, 1.0)"):
        logging.info("inserting orderings into Redis")
        for i in all_entries("sorts"):
            for j in all_entries(i):
                for k in all_entries(j):
                    if all_entries(k):
                        for pickles in all_entries(k):
                            print(f"loading {pickles}")
                            redis.set(
                                f"sorts:{tuple(
                                    map(float, pickles.parts[1:-1])
                                    )!s}",
                                pickles.read_bytes(),
                            )
