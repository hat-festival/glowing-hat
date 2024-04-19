from glowing_hat.mode import Mode


class Off(Mode):
    """Kill the lights."""

    def run(self):
        """Do the stuff."""
        self.hat.off()
