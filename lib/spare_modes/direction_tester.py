from lib.axis_manager import AxisManager
from lib.logger import logging
from lib.mode import Mode
from lib.sorts_generator import SortsGenerator


class DirectionTester(Mode):
    """Test the axes' orientation."""

    def __init__(self, hat, custodian):
        """Construct."""
        super().__init__(hat, custodian)
        self.jump = self.conf["jump"]
        self.steps = self.conf["steps"]
        self.colours = [[255, 0, 255]] * 5 + [[0, 0, 0]] * 95

    def reconfigure(self):
        """Configure ourself."""
        self.manager = AxisManager()

        self.rotator = SortsGenerator("x", "y")
        self.rotator.make_circle(altitude=1.0)

    def run(self):
        """Do the stuff."""
        self.reconfigure()
        key = self.rotator.next
        logging.debug(key)
        self.hat.pixels = self.manager.get_sort(key)

        count = 0
        while True:
            self.hat.illuminate(list(self.colours))
            count += 1
            if count == self.conf["axis-rotate-at"]:
                key = self.rotator.next
                logging.debug(key)
                self.hat.pixels = self.manager.get_sort(key)
                count = 0
