import platform
import socket

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

    def update(self):
        """Update ourself."""
        gen = ImageGenerator(self.custodian, self.conf)
        gen.generate()
        self.display.image(gen.image)
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


class ImageGenerator:
    """Generate an image for the Oled."""

    def __init__(self, custodian, conf):
        """Construct."""
        self.custodian = custodian
        self.conf = conf
        self.width = self.conf["size"]["x"]
        self.height = self.conf["size"]["y"]

        self.font = ImageFont.truetype(
            font=f"fonts/{self.conf['font']['name']}.ttf",
            size=self.conf["font"]["size"],
        )
        self.image = None
        self.draw = None

    def set_image(self, width, height):
        """Set up our image."""
        self.image = Image.new("1", (width, height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0, 0, width, height), outline=0, fill=0)

    def generate(self, save_to=None):
        """Make the picture."""
        if self.custodian.get("display-type") == "hat-settings":
            self.set_image(self.width, self.height)

            self.add_text(self.custodian.get("mode"), 0, 0)

            source = self.custodian.get("colour-source")
            if source == "redis":
                self.add_text(
                    (
                        f"{self.custodian.get('colour-set')}"
                        f"{self.conf['characters']['separator']}"
                        f"{self.hex_colour()}"
                    ),
                    0,
                    self.height / 2,
                )

            else:
                self.add_text(source, 0, self.height / 2)

            self.add_text(
                (
                    f"{self.custodian.get('axis')}"
                    f"{self.conf['characters']['separator']}"
                    f"{self.get_direction()}"
                ),
                104,
                0,
            )

        if self.custodian.get("display-type") == "button-config":
            self.set_image(self.height, self.width)

            for index, abbreviation in enumerate(
                reversed(list(map(lambda x: x["abbreviation"], conf["buttons"])))
            ):
                y_pos = index * 28
                self.add_text(abbreviation, 0, y_pos)
                self.add_text("----", 0, y_pos + 14)

            self.image = self.image.rotate(90, expand=True)

        if self.custodian.get("display-type") == "ip-address":
            self.set_image(self.width, self.height)

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))

            hostname = socket.gethostname()
            ipaddress = sock.getsockname()[0]

            self.add_text(hostname, 0, 0)
            self.add_text(ipaddress, 0, self.height / 2)

        if save_to:
            self.image.save(f"tmp/{save_to}.png")

    def hex_colour(self):
        """Get a hex-colour."""
        colour = ""
        for byte in self.custodian.get("colour"):
            colour += f"{byte:02x}"
        return f"#{colour}"

    def get_direction(self):
        """Get the inversion direction."""
        direction = self.conf["characters"]["up"]
        if self.custodian.get("invert"):
            direction = self.conf["characters"]["up"]

        return direction

    def add_text(self, text, across, down):
        """Add some text."""
        self.draw.text((across, down), text.lower(), font=self.font, fill=255)
