import redis

from lib.tools import make_key


def next_mode(namespace):
    """Get the next mode."""
    rds = redis.Redis()
    current_mode = rds.get(make_key("mode", namespace)).decode()
    modes = list(
        map(lambda x: x.decode(), rds.lrange(make_key("modes", namespace), 0, -1))
    )
    index = modes.index(current_mode)
    rds.set(make_key("mode", namespace), modes[(index + 1) % len(modes)])


if __name__ == "__main__":
    next_mode("hat")
