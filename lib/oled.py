import platform
from random import randint

from PIL import Image, ImageDraw, ImageFont

from lib.conf import conf
from lib.custodian import Custodian

if "arm" in platform.platform():  # nocov
    import adafruit_ssd1306
    import busio
    from board import SCL, SDA


class Oled:
    """Class wrapping the PiOLED display."""

    def __init__(self):
        """Construct."""
        self.conf = conf["oled"]
        self.custodian = Custodian()

        if "arm" in platform.platform():
            i2c = busio.I2C(SCL, SDA)
            self.display = adafruit_ssd1306.SSD1306_I2C(
                self.conf["size"]["x"], self.conf["size"]["y"], i2c
            )

        else:
            self.display = FakeDisplay()

        self.font = ImageFont.truetype(
            font=f"fonts/{self.conf['font']['name']}.ttf",
            size=self.conf["font"]["size"],
        )

        self.image = Image.new("1", (self.display.width, self.display.height))
        self.draw = ImageDraw.Draw(self.image)

    def update(self):
        """Read and display data from Redis."""
        # clear the board
        self.draw.rectangle(
            (0, 0, self.display.width, self.display.height), outline=0, fill=0
        )

        direction = "↑"
        if self.custodian.get("invert"):
            direction = "↓"

        self.put_text(f"{self.custodian.get('mode')}", 0, 0)

        source = self.custodian.get("colour-source")
        if source == "redis":
            self.put_text(
                (
                    f"{self.custodian.get('colour-set')}/"
                    f"#{''.join(f'{i:02x}' for i in self.custodian.get('colour'))}"
                ),
                0,
                self.display.height / 2,
            )

        else:
            self.put_text(source, 0, self.display.height / 2)

        self.put_text(
            f"{self.custodian.get('axis')}/{direction}", self.conf["offset"], 0
        )

        self.display.image(self.image)
        self.display.show()

    def flash(self):
        """Blank the screen."""
        self.draw.rectangle(
            (0, 0, self.display.width, self.display.height), outline=0, fill=0
        )

        for _ in range(256):
            self.draw.point(
                (
                    randint(0, self.display.width - 1),
                    randint(0, self.display.height - 1),
                ),
                1,
            )

        self.display.image(self.image)
        self.display.show()

    def put_text(self, text, across, down):
        """Draw some text."""
        self.draw.text((across, down), text.lower(), font=self.font, fill=255)


class FakeDisplay:
    """Fake OLED for testing."""

    def __init__(self):
        """Construct."""
        self.width = self.height = 1

    def image(self, _):
        """Do something."""

    def show(self):
        """Show something."""
