from datetime import datetime
from time import sleep

from glowing_hat.mode import Mode


class Clock(Mode):
    """A binary clock."""

    def run(self):
        """Do the stuff."""
        self.hat.off()

        while True:
            self.write_time(datetime.now())  # noqa: DTZ005
            sleep(0.1)

    def write_time(self, timestamp):
        """Display the time."""
        self.binaries = binary_hms(timestamp)
        self.accumulator = 0

        self.draw_divider()
        for key in reversed(self.binaries):
            self.draw_section(key)
            self.draw_divider()

        for pixel in self.hat.pixels[0:21]:
            other_index = (len(self.hat) - 1) - pixel["index"]
            self.hat.apply_hue_to_one_pixel(other_index, pixel["hue"])
            self.hat.apply_value_to_one_pixel(other_index, pixel["value"])
            self.hat.apply_saturation_to_one_pixel(other_index, pixel["saturation"])

        self.hat.light_up()

    def draw_section(self, section):
        """Draw a section."""
        vals = list(reversed(bin_string_to_values(self.binaries[section])))
        for index in range(len(vals)):
            self.hat.apply_hue_to_one_pixel(
                self.accumulator, self.conf["hues"][section]
            )
            self.hat.apply_value_to_one_pixel(self.accumulator, vals[index])
            self.accumulator += 1


def bin_string_to_values(string):
    """Convert a binary-string to some values."""
    return list(map(float, string))


def binary_hms(timestamp):
    """Get the binary pieces of a timestamp."""
    return {
        "hours": f"{timestamp.hour:>05b}",
        "minutes": f"{timestamp.minute:>06b}",
        "seconds": f"{timestamp.second:>06b}",
    }
