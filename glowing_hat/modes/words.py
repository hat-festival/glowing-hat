from pathlib import Path
from time import sleep

import yaml

from glowing_hat.arrangements.word_streamer import WordStreamer
from glowing_hat.custodian import Custodian
from glowing_hat.hue_sources.time_based_hue_source import TimeBasedHueSource
from glowing_hat.mode import Mode
from glowing_hat.shitpost_language_model import ShitPostLanguageModel
from glowing_hat.tools.logger import logging


class Words(Mode):
    """Write some words."""

    # TODO: get the pikesley_ebooks toots
    def configure(self):
        """Configure."""
        self.hat.off()
        self.custodian = Custodian(conf=self.conf, namespace="hat")
        self.strings = yaml.safe_load(
            Path("conf", "panel", "strings.yaml").read_text(encoding="utf-8")
        )

        key = self.custodian.get("string")

        self.splm = None
        if key == "splm":
            logging.debug("we are shitposting")
            self.splm = ShitPostLanguageModel()
            content = self.splm.generate()
            logging.debug("content is `%s`", content)
            self.word_streamer = WordStreamer(content)

        else:
            content = self.strings[key]
            self.word_streamer = WordStreamer(content)

        self.hue_source = TimeBasedHueSource(self.conf["hue-change-speed"])
        self.hat.sort("x")

    def run(self):
        """Do stuff."""
        self.configure()

        while True:
            for frame in self.word_streamer:
                self.render_frame(frame)

                self.hat.light_up()
                sleep(self.conf["delay"])

            if self.splm:
                content = self.splm.generate()
                logging.debug("Content is `%s`", content)
                self.word_streamer = WordStreamer(content)
            else:
                self.word_streamer.reset()

    def render_frame(self, frame):
        """Render one frame."""
        for i in range(32):
            for j in range(8):
                val_hue = (1, self.hue_source.hue())
                if frame[i][j] == 0:
                    val_hue = (
                        self.conf["inverse-value"],
                        self.hue_source.inverse_hue(),
                    )

                self.hat.pixels[j + (i * 8)]["value"] = frame[i][j]

                pixel = self.hat.pixels[j + (i * 8)]
                pixel["value"], pixel["hue"] = val_hue
