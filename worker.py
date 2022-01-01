import json
from time import sleep

import redis

from lib.hat import Hat


class Worker:
    """Worker to process the jobs."""

    def __init__(self):
        """Construct."""
        self.redis = redis.Redis()
        self.hat = Hat()

    def process(self, job):
        """Process a job."""
        try:
            data = json.loads(job.decode("utf-8"))
            self.hat.light_all(data["colour"])

        except (json.decoder.JSONDecodeError, KeyError):  # nocov
            print("Your data is bad")

    def poll(self):
        """If there's a job on the queue, pull it off and process it."""
        data = self.redis.lpop("jobs")
        if data:
            self.process(data)

        else:  # nocov
            sleep(0.1)

    def work(self):  # nocov
        """Keep working forever."""
        while True:
            self.poll()


if __name__ == "__main__":  # nocov
    print("worker starting")
    worker = Worker()
    worker.work()
