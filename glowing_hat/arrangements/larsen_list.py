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

        self.sections = {
            "right": {
                "lead": self.create_lead(),
                "chaser": self.create_chaser(),
                "complete": self.create_lead() + self.create_chaser(),
            },
            "left": {
                "lead": self.create_lead(inverted=True),
                "chaser": self.create_chaser(inverted=True),
                "complete": self.create_lead(inverted=True)
                + self.create_chaser(inverted=True),
            },
            "both": {
                "complete": self.create_lead()
                + self.create_chaser()
                + self.create_lead(inverted=True)
                + self.create_chaser(inverted=True),
            },
        }

    def get_iterator(self, direction, piece, infinite=False):  # noqa: FBT002
        """Get an iterator for a piece."""
        return LarsenIterator(self.sections[direction][piece], infinite)

    def prepare_template(self):
        """Prepare the full snake."""
        start_value = 1.0
        self.template = {"head": [start_value] * self.head_steps, "tail": []}

        tail = []
        step_size = int(100 / (self.tail_proportion * self.hat_length))
        for value in range(100, 0, 0 - step_size):
            intensity = value * start_value / 100
            if intensity != start_value:
                tail.append(intensity)

        tail.reverse()
        self.template["tail"] = tail

    def create_lead(self, inverted=False):  # noqa: FBT002
        """Create the lead portion."""
        intensities = []

        snake = self.lead_snake()

        for _ in range(self.hat_length - (self.head_steps - 1)):
            intensities.append(
                slice_from_end(snake, 0, self.hat_length, inverted=inverted)
            )
            snake.rotate(1)

        return intensities

    def create_chaser(self, inverted=False):  # noqa: FBT002
        """Create the chase portion."""
        intensities = []

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

    def populate(self, inverted=False):  # noqa: FBT002
        """Prepare our data."""
        return self.create_lead(inverted) + self.create_chaser(inverted)

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


class LarsenIterator:
    """Iterate over a piece."""

    def __init__(self, section, infinite=False):  # noqa: FBT002
        """Construct."""
        self.section = section
        self.infinite = infinite
        self.index = 0

    def __iter__(self):
        """Be an iterator."""
        return self

    def __next__(self):
        """Get `next`."""
        if self.has_next():
            frame = self.section[self.index]
            self.index += 1
            return frame

        if self.infinite:
            self.index = 0
            return self.section[self.index]

        raise StopIteration

    def __getitem__(self, index):
        """Get by `[index]`."""
        return self.section[index]

    def has_next(self):
        """Do we have more items."""
        return self.index < len(self.section)

    def reset(self):
        """Start again."""
        self.index = 0


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
