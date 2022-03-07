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
        dimensions = conf["oled-size"]
        self.redisman = redis_manager

        if "arm" in platform.platform():
            i2c = busio.I2C(SCL, SDA)
            self.display = adafruit_ssd1306.SSD1306_I2C(
                dimensions["x"], dimensions["y"], i2c
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

        top = 0
        left = 0
        font = ImageFont.truetype(font='fonts/Hubballi-Regular.ttf', size=18)

        mode = self.redisman.get("mode")
        text = f"mode: {mode.lower()}"
        draw.text((left, top), text, font=font, fill=255)

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
