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
