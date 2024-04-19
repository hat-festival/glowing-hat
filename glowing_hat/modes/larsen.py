from glowing_hat.arrangements.larsen_list import LarsenList
from glowing_hat.mode import Mode


class Larsen(Mode):
    """Larsen scanner."""

    def configure(self):
        """Configure ourself."""
        self.larsen_list = LarsenList(
            len(self.hat),
            head_width=self.conf["head-width"],
            tail_proportion=self.conf["tail-proportion"],
        )

        self.hat.apply_hue(self.conf["hue"])
        self.hat.sort(self.conf["axes"]["movement"])
        self.iterator = self.larsen_list.get_iterator("both", "complete", infinite=True)

    def run(self):
        """Do the stuff."""
        self.configure()

        count = 0
        frame = None
        while True:
            if count % self.conf["jump"] == 0:
                for _ in range(self.conf["jump"]):
                    frame = next(self.iterator)

                self.hat.apply_values(frame)
                self.hat.light_up()
                count = 0

            count += 1
