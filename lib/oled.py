import socket

from PIL import Image, ImageDraw, ImageFont

from lib.conf import conf
from lib.tools import is_pi

if is_pi():  # nocov
    import adafruit_ssd1306
    import busio
    from board import SCL, SDA


class Oled:
    """Class wrapping the PiOLED display."""

    def __init__(self, custodian):
        """Construct."""
        self.conf = conf["oled"]
        self.custodian = custodian

        if is_pi():
            i2c = busio.I2C(SCL, SDA)
            self.display = adafruit_ssd1306.SSD1306_I2C(
                self.conf["size"]["x"], self.conf["size"]["y"], i2c
            )

        else:
            self.display = FakeDisplay()

        self.gen = ImageGenerator(self.custodian, self.conf)

    def update(self):
        """Update ourself."""
        screen = self.gen.generate()
        screen = screen.rotate(180, expand=True)
        self.display.image(screen)
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
        # map redis value to method name
        getattr(self, self.custodian.get("display-type").replace("-", "_"))()

        if save_to:
            self.image.save(f"tmp/{save_to}.png")

        return self.image

    def hat_settings(self):
        """Make the `hat-settings` image."""
        self.set_image(self.width, self.height)

        self.add_text(self.custodian.get("mode"), 0, 0)

        source = self.custodian.get("colour-source")
        if source == "redis":
            self.add_text(
                self.colour_text(),
                0,
                self.height / 2,
            )

        elif source != "none":
            self.add_text(source, 0, self.height / 2)

        self.add_text(
            self.axis_invert(),
            self.width - 24,  # align this to the right
            0,
        )

        self.add_text(
            f"fft: {'on' if self.custodian.get('fft-on') else 'off'}", self.width-72, 16
        )

    def button_config(self):
        """Make the `button-config` image."""
        self.set_image(self.height, self.width)

        items = (
            len(conf["buttons"]) * 2
        ) - 1  # number of buttons, with a divider between each
        step_size = round(self.width / items)

        for index, abbreviation in enumerate(
            reversed(list(map(lambda x: x["abbreviation"], conf["buttons"])))  # noqa: C417
        ):
            self.add_button(abbreviation, index, step_size)

        self.image = self.image.rotate(270, expand=True)

    def ip_address(self):
        """Make the `ip-address` image."""
        self.set_image(self.width, self.height)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))

        hostname = socket.gethostname()
        ipaddress = sock.getsockname()[0]

        self.add_text(hostname, 0, 0)
        self.add_text(ipaddress, 0, self.height / 2)

    def boot(self):
        """Boot-time message."""
        self.set_image(self.width, self.height)

        message = "Hat is booting"
        left = (self.width - (len(message) * 8)) / 2
        top = (self.height - 16) / 2
        self.add_text(message, left, top)

    def hex_colour(self):
        """Get a hex-colour."""
        colour = ""
        for byte in self.custodian.get("colour"):
            colour += f"{byte:02x}"
        return f"#{colour}"

    def get_sign(self):
        """Get the sign of the inversion."""
        return "-" if self.custodian.get("invert") else "+"

    def axis_invert(self):
        """Construct the axis-inversion string."""
        axisless_modes = list(
            dict(
                filter(
                    lambda x: x[1].get("prefs").get("axis") == "none",
                    conf.get("modes").items(),
                )
            ).keys()
        )
        if self.custodian.get("mode") in axisless_modes:
            return ""

        return f"{self.get_sign()}{self.custodian.get('axis')}"

    def add_button(self, text, index, step_size):
        """Add button marker."""
        y_pos = index * step_size * 2
        self.add_text(text, 0, y_pos)
        # https://www.compart.com/en/unicode/U+2015
        self.add_text("――――", 0, y_pos + step_size)

    def colour_text(self):
        """Get the colour-set/hex text."""
        return (
            f"{self.custodian.get('colour-set')}"
            f"{self.conf['characters']['separator']}"
            f"{self.hex_colour()}"
        )

    def add_text(self, text, across, down):
        """Add some text."""
        self.draw.text((across, down), text.lower(), font=self.font, fill=255)
