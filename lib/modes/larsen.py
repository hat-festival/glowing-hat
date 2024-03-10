from collections import deque

from lib.arrangements.larsen_list import LarsenList
from lib.mode import Mode
from lib.tools import scale_colour


class Larsen(Mode):
    """Larsen scanner."""

    def configure(self):
        """Configure ourself."""
        self.jump = self.data["jump"]
        self.values = deque()
        self.larsen_list = LarsenList(
            len(self.hat),
            head_width=self.data["head-width"],
            tail_proportion=self.data["tail-proportion"],
        )

        self.hat.sort("x")

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            clr = self.get_colour()
            self.from_list(
                list(  # noqa: C417
                    map(
                        lambda x: scale_colour(clr, x), self.larsen_list.next(self.jump)
                    )
                )
            )
