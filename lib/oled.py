import platform

from PIL import Image, ImageDraw, ImageFont

from lib.conf import conf

if "arm" in platform.platform():  # nocov
    import adafruit_ssd1306
    import busio
    from board import SCL, SDA


class Oled:
    """Class wrapping the PiOLED display."""

    def __init__(self, redis_manager):
        """Construct."""
        self.conf = conf["oled"]
        self.redisman = redis_manager

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
        if self.redisman.get("invert") == "true":
            direction = "↓"

        self.put_text(f"{self.redisman.get('mode')}", 0, 0)

        self.put_text(
            (
                f"{self.redisman.get('roller')}/"
                f"#{''.join(f'{i:02x}' for i in self.redisman.get_colour())}"
            ),
            0,
            self.display.height / 2,
        )
        self.put_text(
            f"{self.redisman.get('axis')}/{direction}", self.conf["offset"], 0
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
