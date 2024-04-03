from lib.arrangements.circle import Circle
from lib.arrangements.rolling_queue import RollingQueue
from lib.mode import Mode


class Spotlights(Mode):
    """Subtly rolling."""

    def configure(self):
        """Configure ourself."""
        self.circles = []
        self.rollers = []
        self.hues = []

        for i in range(self.conf["spots"]):
            self.circles.append(
                Circle(*self.conf["axes"], steps=self.conf["step-size"])
            )
            self.rollers.append(RollingQueue(length=self.conf["queue-length"]))
            self.hues.append((1 / self.conf["spots"]) * i)

        for i in range(self.conf["spots"]):
            for _ in range(
                int(
                    len(self.circles[i].rotator.hoop)
                    / self.conf["spots"]
                    / self.conf["step-size"]
                )
                * i
            ):
                self.circles[i].next()

        for _ in range(self.conf["queue-length"]):
            for i in range(self.conf["spots"]):
                self.rollers[i].push(self.circles[i].next())

    def run(self):
        """Do the work."""
        self.configure()

        self.hat.off()

        while True:
            self.hat.apply_value(1.0)
            self.hat.apply_saturation(0.0)

            for outer_index in range(len(self.rollers[0])):
                for i in range(self.conf["spots"]):
                    sort = self.rollers[i][outer_index]

                    for index in sort[0 : self.conf["spot-size"]]:
                        pixel = self.hat.pixels[index]
                        pixel["hue"] = self.hues[i]
                        pixel["value"] = outer_index / self.conf["queue-length"]
                        pixel["saturation"] = 1.0
                        self.hat.light_one(pixel)

            self.hat.light_up()

            for i in range(self.conf["spots"]):
                self.rollers[i].push(self.circles[i].next())
