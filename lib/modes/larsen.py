from collections import deque

from lib.arrangements.larsen_list import LarsenList
from lib.mode import Mode
from lib.tools import scale_colour


class Larsen(Mode):
    """Larsen scanner."""

    def configure(self):
        """Configure ourself."""
        self.values = deque()
        self.larsen_list = LarsenList(
            len(self.hat),
            head_width=self.data["head-width"],
            tail_proportion=self.data["tail-proportion"],
        )

        self.hat.sort(self.data["axes"]["movement"])
        self.iterator = self.larsen_list.get_iterator("both", "complete", infinite=True)

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            clr = self.get_colour()
            colours = list(  # noqa: C417
                map(lambda x: scale_colour(clr, x), next(self.iterator))
            )
            for index, pixel in enumerate(self.hat.pixels):
                colours[index] = scale_colour(
                    colours[index], ((pixel[self.data["axes"]["fade"]] + 1) / 2)
                )
            self.from_list(colours)
