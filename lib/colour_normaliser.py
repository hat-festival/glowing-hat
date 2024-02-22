from collections import deque
from multiprocessing import Process

from lib.colour_scalers.fourier_transformer import FourierTransformer
from lib.colour_scalers.rotary_encoder import RotatingScaler
from lib.conf import conf
from lib.gamma import gamma


class ColourNormaliser:
    """Normalises colours."""

    def __init__(self):
        """Construct."""
        self.max_brightness = conf["max-brightness"]
        self.default_brightness = self.max_brightness * 0.2
        self.step_size = 0.02
        self.scaler_proc = None
        self.scalers = deque(
            [
                FourierTransformer(self),
                RotatingScaler(self),
            ]
        )

    def run(self):
        """Do the work."""
        if self.scaler_proc and self.scaler_proc.is_alive():
            self.scaler_proc.terminate()

        self.scaler_proc = Process(target=self.scalers[0].run)
        self.scaler_proc.start()
        self.scalers.rotate()

    def normalise(self, triple):
        """Normalise a colour."""
        return tuple(int(x * self.factor.value) for x in gamma_correct(triple))


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return tuple(map(lambda n: gamma[int(n)], triple))  # noqa: C417
