from multiprocessing import Process, Value
from time import sleep

from lib.fourier import Fourier
from lib.mode import Mode
from lib.renderers.sweeper import angle  # TODO rehome this to tools?
from lib.tools import hue_to_rgb, scale_colour


class Equaliser(Mode):
    """Equalise."""

    def configure(self):
        """Configure ourself."""
        self.decay_amount = self.data["decay"]["amount"]
        self.decay_interval = self.data["decay"]["interval"]

        self.max_y = self.data["y"]["max"]
        self.default_y = Value("f", self.data["y"]["default"])
        self.active_y = Value("f", self.default_y.value)

        self.fft = Fourier(self)
        self.fft_proc = Process(target=self.fft.transform)
        self.reducer_proc = Process(target=self.reduce)

        self.reducer_proc.start()
        self.fft_proc.start()

    def run(self):
        """Do the sork."""
        self.configure()

        rotation = 90
        print(self.data)
        while True:
            self.hues = []
            for pix in self.hat.pixels:
                pix["angle"] = (angle(pix["x"], pix["z"]) - rotation) % 360
                pix["hue"] = pix["angle"] / 360
            rotation = (rotation + self.data["rotation"]) % 360

            lights = []
            for pixel in self.hat.pixels:
                colour = hue_to_rgb(pixel["hue"])
                if pixel["y"] < self.active_y.value:
                    lights.append(colour)
                else:
                    lights.append(scale_colour(colour, self.data["scale-factor"]))

            self.from_list(lights)

    def trigger(self):
        """Spike our `y`. Called by our FFT."""
        self.active_y.value = self.max_y

    def reduce(self):
        """Constantly reducing the `y`."""
        while True:
            if self.active_y.value > self.default_y.value:
                self.active_y.value -= self.decay_amount
                sleep(self.decay_interval)
