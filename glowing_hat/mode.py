from glowing_hat.conf import conf


class Mode:
    """Superclass for `modes`."""

    def __init__(self, hat):
        """Construct."""
        self.hat = hat
        self.name = type(self).__name__.lower()
        try:
            self.conf = conf.get("modes").get(self.name)
        except AttributeError:
            self.conf = {}

    def draw_divider(self, width=1):
        """Draw a divider."""
        for _ in range(width):
            self.hat.apply_value_to_one_pixel(self.accumulator, 1.0)
            self.hat.apply_saturation_to_one_pixel(self.accumulator, 0.0)
            self.accumulator += 1
