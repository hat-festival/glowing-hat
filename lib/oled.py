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

    def update(self):
        """Read and display data from Redis."""
        width = self.display.width
        height = self.display.height
        image = Image.new("1", (width, height))
        draw = ImageDraw.Draw(image)

        # clear the board
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        font = ImageFont.truetype(
            font=f"fonts/{self.conf['font']['name']}.ttf",
            size=self.conf["font"]["size"],
        )

        mode = f"m: {self.redisman.get('mode')}"
        draw.text((0, 0), mode.lower(), font=font, fill=255)

        colour = f"c: {self.redisman.get('colour')}"
        draw.text((80, 0), colour.lower(), font=font, fill=255)

        axis = f"a: {self.redisman.get('axis')}"
        draw.text((0, 16), axis.lower(), font=font, fill=255)

        invert = f"i: {self.redisman.get('invert')}"
        draw.text((80, 16), invert.lower(), font=font, fill=255)

        self.display.image(image)
        self.display.show()


class FakeDisplay:
    """Fake OLED for testing."""

    def __init__(self):
        """Construct."""
        self.width = self.height = 1

    def image(self, _):
        """Do something."""

    def show(self):
        """Show something."""
