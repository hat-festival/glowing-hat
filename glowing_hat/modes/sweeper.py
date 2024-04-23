import pickle
import random
from collections import deque
from pathlib import Path

from glowing_hat.mode import Mode


class Sweeper(Mode):
    """Sweeper mode."""

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.frames = pickle.loads(  # noqa: S301
            Path("renders", "radar.pickle").read_bytes()
        )

        # we have this here to make it testable
        self.max_laps = None

        self.blips = [Blip(self.hat, self.conf)]

    def run(self):
        """Do the work."""
        laps = 0

        while True:
            for count, values in enumerate(self.frames):
                if count % self.conf["jump"] == 0:
                    self.make_frame(values)

            if self.max_laps:
                laps += 1

                if laps == self.max_laps:
                    break

            self.cycle_blips()

            if len(self.blips) < self.conf["blip-count"]:
                self.blips.append(Blip(self.hat, self.conf))

    def make_frame(self, values):
        """Make one frame."""
        self.hat.apply_values(values)
        self.hat.apply_hue(self.conf["hues"]["main"])

        for blip in self.blips:
            if blip.is_visible(values):
                self.hat.pixels[blip.index]["hue"] = self.conf["hues"]["blip"]

        self.hat.light_up()

    def cycle_blips(self):
        """Cycle the blips."""
        for blip in self.blips:
            blip.cycle()


class Blip:
    """A blip."""

    def __init__(self, hat, conf):
        """Construct."""
        self.conf = conf
        self.hat_length = len(hat)
        self.index = random.randint(0, self.hat_length - 1)  # noqa: S311
        self.high_value = 0.9
        self.low_value = 0.1
        self.show = False

        self.states = deque(
            [
                {"name": "blank", "show-blip": False, "side-effect": self.move},
                {"name": "entry", "show-blip": False},
                {"name": "regular", "show-blip": True, "condition": self.expire},
                {"name": "exit", "show-blip": True},
            ]
        )

        self.state = self.states[0]

    def is_visible(self, values):
        """Determine whether to reveal ourselves."""
        self.reveal(values)
        self.hide(values)

        return self.show

    def reveal(self, values):
        """Determine when to reveal ourself on an `entry` lap."""
        if self.state["name"] == "entry" and values[self.index] > self.high_value:
            self.show = True

    def hide(self, values):
        """Determine when to hide ourself on an `exit` lap."""
        if self.state["name"] == "exit" and values[self.index] < self.low_value:
            self.show = False

    def cycle(self):
        """Advance through our lifecycle."""
        if self.state.get("condition", lambda: True)():
            self.states.rotate(-1)
            self.state = self.states[0]

        self.state.get("side-effect", lambda: None)()

    def move(self):
        """Move us."""
        self.index = random.randint(0, self.hat_length - 1)  # noqa: S311

    def expire(self):
        """Expire ourself maybe."""
        return random.random() > self.conf["blip-move-threshold"]  # noqa: S311
