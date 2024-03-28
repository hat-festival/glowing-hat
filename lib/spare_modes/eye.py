from time import sleep

from lib.arrangements.larsen_list import LarsenList
from lib.mode import Mode
from lib.sorters.axis_manager import AxisManager
from lib.sorters.sort_key import SortKey
from lib.tools.utils import scale_colour


class Eye(Mode):
    """Moving eye."""

    def configure(self):
        """Configure ourself."""
        self.am = AxisManager()

        self.larsen_list = LarsenList(
            len(self.hat),
            head_width=0.3,
            tail_proportion=0.9,
        )

        colour = [255, 0, 0]
        larsen_iterator = self.larsen_list.get_iterator("left", "chaser")
        frame = larsen_iterator[70]
        self.colours = list(  # noqa: C417
            map(lambda x: scale_colour(colour, x), frame)
        )

        lower_limit = -7
        upper_limit = 11

        self.iterators = {
            "right": list(range(lower_limit, upper_limit, 1)),
            "left": list(range(upper_limit, lower_limit, -1)),
        }

        self.delay = 0.03

    def run(self):
        """Do the work."""
        self.configure()

        while True:
            for iterator in self.iterators.values():
                for item in iterator:
                    self.from_sort(key_from_x(item))
                    self.from_list(self.colours)
                    sleep(self.delay)

            sleep(0.5)


def key_from_x(x):
    """Construct a key."""
    altitude = 0.2
    return SortKey(x / 10, altitude, 1.0).as_key
