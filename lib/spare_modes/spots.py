from random import choice

from lib.hue_sources.time_based_hue_source import TimeBasedHueSource
from lib.mode import Mode
from lib.sorters.axis_manager import AxisManager


class Spots(Mode):
    """Spots."""

    def configure(self):
        """Configure."""
        self.hue_source = TimeBasedHueSource()
        self.manager = AxisManager()
        self.axes = {"x": 1.0, "y": 1.0, "z": 1.0}

        self.favoured_axis = "x"
        self.favoured_increment = 0.1  # positive

        self.weighting = 0.9  # conf this

    def run(self):
        """Do the stuff."""
        self.configure()

        while True:
            sort = self.get_next_sort()

            hue = self.hue_source.hue()

            self.hat.apply_value(0.5)
            for index in sort[0:50]:
                pixel = self.hat.pixels[index]
                pixel["hue"] = hue
                pixel["value"] = 1.0
                self.hat.light_one(pixel)

            self.hat.light_up()

    def get_next_sort(self):
        """Get a random `sort`."""
        # TODO can we map this to a `sin` curve or sth?
        # TODO we can drive this with tests
        # if random() > self.weighting:
        #     self.favoured_axis = choice(tuple(self.axes.keys()))

        # if random() > self.weighting:
        #     self.favoured_increment = choice([-0.1, 0.1])

        # if self.axes[self.favoured_axis] == 1.0 and self.favoured_increment == 0.1 or self.axes[self.favoured_axis] == -1.0 and self.favoured_increment == -0.1:  # noqa: E501
        #     self.favoured_axis = choice(tuple(self.axes.keys()))

        # self.axes[self.favoured_axis] = round(self.axes[self.favoured_axis] + self.favoured_increment, 1)  # noqa: E501
        # from lib.tools.logger import logging
        # logging.debug(self.axes)

        axis = choice(tuple(self.axes.keys()))  # noqa: S311
        if self.axes[axis] == 1.0:
            self.axes[axis] = 0.9
        elif self.axes[axis] == -1.0:
            self.axes[axis] = -0.9
        else:
            self.axes[axis] = round(self.axes[axis] + choice([-0.1, 0.1]), 1)  # noqa: S311

        return self.manager.get_sort(tuple(self.axes.values()))
