from pathlib import Path

import yaml
from anyascii import anyascii

characters = yaml.safe_load(
    Path("conf", "panel", "characters.yaml").read_text(encoding="utf-8")
)


class WordStreamer:
    """Stream words."""

    def __init__(self, string, width=4):
        """Construct."""
        self.string = string
        self.width = width
        self.word_iterator = WordIterator(self.string, self.width)
        self.substring = None
        self.counter = 0

    def __iter__(self):
        """Be an iterator."""
        return self

    def __next__(self):
        """Get `next`."""
        if self.word_iterator.done:
            raise StopIteration

        if self.counter == 0:
            self.substring = next(self.word_iterator)

        data = to_bits(self.substring)
        chunk = data[self.counter : self.counter + 32]
        self.counter += 1

        if self.counter == 8:  # noqa: PLR2004
            self.counter = 0

        return chunk

    def reset(self):
        """Go again."""
        self.word_iterator = WordIterator(self.string, self.width)


class WordIterator:
    """Iterate over a string."""

    def __init__(self, string, width):
        """Construct."""
        self.width = width + 1
        self.string = " " * (self.width - 1) + string + " " * self.width
        self.index = 0
        self.done = False

    def __iter__(self):
        """Be an iterator."""
        return self

    def __next__(self):
        """Get `next`."""
        if self.done:
            raise StopIteration

        frame = self.string[self.index : self.index + self.width]
        if all(x == frame[0] for x in frame):
            self.done = True

        self.index += 1
        return frame


def char_to_bits(character):
    """Turn character into bitstrings."""
    if character not in ["©"]:
        character = anyascii(character)
    return [
        list(map(int, list(f"{x:#010b}"[2:]))) for x in characters[character]
    ]


def to_bits(string):
    """Turn string into bitstrings."""
    rack = [[] for _ in range(8)]

    for char in string:
        bits = char_to_bits(char)
        for index, bitstring in enumerate(bits):
            rack[index] += bitstring

    return [[row[index] for row in rack] for index in range(len(string * 8))]
