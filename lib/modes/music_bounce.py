from multiprocessing import Process

from lib.mode import Mode
from lib.tools import scale_colour


class MusicBounce(Mode):
    """Responding to some value in Redis?."""

    def reconfigure(self):
        """Configure ourself."""
        self.sort_hat()

    def run(self):
        """Do the stuff."""
        self.reconfigure()

        drums = {
            # "high": {"colour": (255, 0, 0), "value": 0, "new_value": 0},
            # "mid": {"colour": (0, 255, 0), "value": 0, "new_value": 0},
            "low": {"colour": (0, 0, 255), "value": 0, "new_value": 0},
        }

        process = None
        while True:
            for pitch, data in drums.items():
                data["new_value"] = self.custodian.get(pitch)
                if data["value"] != data["new_value"]:
                    if process and process.is_alive():
                        process.terminate()

                    process = Process(target=self.punch)
                    process.start()
                    data["value"] = data["new_value"]

    def punch(self):
        """Illuminate the hat."""
        colour = self.get_colour()
        for i in range(100, 50, -2):
            colour = scale_colour(colour, i / 100)
            self.hat.fill(colour)
            # sleep(0.     01)
