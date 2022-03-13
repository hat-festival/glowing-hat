# noqa
import pickle
from collections import deque
from pathlib import Path

from lib.mode import Mode

# from lib.tools import scale_colour


class Larsen(Mode):
    """Larsen scanner."""

    # can this go in the superclass?
    frame_sets = pickle.loads(Path("renders/bands.pickle").read_bytes())

    def __init__(self, hat):
        """Construct."""
        super().__init__(hat)

        self.data = {
            "there": {"lead": [], "tail": []},
            # "back": {"lead": [], "tail": []},
        }

        frames_key = f"{self.axis}_up"
        frames = Larsen.frame_sets[frames_key]
        self.data["there"]["lead"] = deque(frames)

        up_tail = deque(frames)
        up_tail.rotate(0 - self.conf["modes"][self.name]["offset"])
        self.data["there"]["tail"] = up_tail

        # frames_key = f"{self.axis}_down"
        # frames = Larsen.frame_sets[frames_key]
        # self.data["back"]["lead"] = deque(frames)

        # down_tail = deque(frames)
        # down_tail.rotate(self.conf["modes"][self.name]["offset"])
        # self.data["back"]["tail"] = down_tail

    def run(self):
        """Do the stuff."""
        self.hat.off()

        while True:
            for _, things in self.data.items():
                colour = self.get_colour()
                # tail_colour = scale_colour(colour, 0.1)
                for index in range(len(things["lead"])):
                    if index % self.conf["modes"][self.name]["steps"] == 0:
                        lead_lights = things["lead"][index]
                        self.hat.colour_indeces(
                            list(map(lambda x: x["index"], lead_lights)),
                            colour,
                            auto_show=False,
                        )

                        tail_lights = things["tail"][index]
                        self.hat.colour_indeces(
                            list(map(lambda x: x["index"], tail_lights)),
                            [0, 255, 0],
                            auto_show=False,
                        )

                        # self.hat.colour_indeces(
                        #     list(map(lambda x: x["index"], things["tail"][index])),
                        #     tail_colour,
                        #     auto_show=False,
                        # )

                        self.hat.show()
