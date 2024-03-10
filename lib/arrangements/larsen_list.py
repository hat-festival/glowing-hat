from collections import deque


class LarsenList:
    """Intensity values for a Larsen Scanner."""

    def __init__(self, hat_length, tail_proportion=1.0, head_width=0.1):
        """Construct."""
        self.hat_length = hat_length
        self.tail_proportion = tail_proportion
        self.head_width = head_width
        self.head_steps = int(self.head_width * self.hat_length)
        self.prepare_template()
        self.intensities = deque(self.populate() + self.populate(inverted=True))

    def next(self, steps=1):
        """Keep sending frames."""
        frame = self.intensities[0]
        self.intensities.rotate(0 - steps)

        return frame

    def prepare_template(self):
        """Prepare the full snake."""
        start_value = 1.0
        self.template = {"head": [start_value] * self.head_steps, "tail": []}

        tail = []
        for value in range(
            100, 0, 0 - int(1 / self.tail_proportion * 100 / self.hat_length)
        ):
            intensity = value * start_value / 100
            if intensity != start_value:
                tail.append(intensity)

        tail.reverse()
        self.template["tail"] = tail

    def populate(self, inverted=False):  # noqa: FBT002
        """Prepare our data."""
        intensities = []

        snake = self.lead_snake()

        for _ in range(self.hat_length - (self.head_steps - 1)):
            intensities.append(
                slice_from_end(snake, 0, self.hat_length, inverted=inverted)
            )
            snake.rotate(1)

        # second phase
        snake = self.chaser_snake(inverted)

        for _ in range(len(self.template["tail"])):
            if inverted:
                snake.rotate(-1)
                piece = slice_from_start(snake, 0, self.hat_length - self.head_steps)
            else:
                snake.rotate(1)
                piece = slice_from_end(snake, 0, self.hat_length - self.head_steps)

            chunk = piece + self.template["head"]
            if inverted:
                chunk = self.template["head"] + piece

            intensities.append(chunk)

        return intensities

    def lead_snake(self):
        """Make the lead snake."""
        return deque(
            self.template["tail"]
            + self.template["head"]
            + [0.0] * (self.hat_length - self.head_steps)
        )

    def chaser_snake(self, inverted=False):  # noqa: FBT002
        """Make the chaser snake."""
        snake = deque(
            [0.0] * (self.hat_length - self.head_steps) + self.template["tail"]
        )

        if inverted:
            snake.reverse()

        return snake


def slice_from_start(iterable, start, length):
    """Chop a piece out of an iterable from the front."""
    return list(iterable)[start : start + length]


def slice_from_end(iterable, end, length, inverted=False):  # noqa: FBT002
    """Chop a piece out of an iterable from the back."""
    end_index = end if end > 0 else None
    piece = list(iterable)[end - length : end_index]

    if inverted:
        piece.reverse()

    return piece
