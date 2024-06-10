from collections import deque


class TempoQueue:
    """Tempo queue."""

    def __init__(self, length):
        """Construct."""
        self.length = length
        self.queue = deque([0] * self.length)

    def add(self, item):
        """Add something."""
        self.queue.pop()
        self.queue.appendleft(item)

    @property
    def interval(self):
        """Get the average interval."""
        gaps = [
            self.queue[index] - self.queue[index + 1]
            for index in range(len(self.queue) - 1)
        ]

        return sum(gaps) / len(gaps)

    @property
    def tempo(self):
        """Get the tempo."""
        tempo = 60 / self.interval
        if tempo < 1:
            return None

        return tempo
