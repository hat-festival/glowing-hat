import socket

from PIL import Image, ImageDraw, ImageFont

from glowing_hat.conf import conf
from glowing_hat.tools.utils import current_ssid, is_pi

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

        self.display = FakeDisplay()
        if is_pi():
            try:
                i2c = busio.I2C(SCL, SDA)
                self.display = adafruit_ssd1306.SSD1306_I2C(
                    self.conf["size"]["x"], self.conf["size"]["y"], i2c
                )

            except ValueError:
                pass

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
        self.offsets = self.conf["offsets"]

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
        display_type = self.custodian.get("display-type")
        if not display_type:
            display_type = "boot"

        getattr(self, display_type.replace("-", "_"))()

        if save_to:
            self.image.save(f"tmp/{save_to}.png")

        return self.image

    def show_mode(self):
        """Make the `show-mode` image."""
        self.set_image(self.width, self.height)
        self.add_text(self.custodian.get("mode"), self.offsets["x"], self.offsets["y"])
        self.draw_brightness_bar()

    def ip_address(self):
        """Make the `ip-address` image."""
        self.set_image(self.width, self.height)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))

        ipaddress = sock.getsockname()[0]

        self.add_text(
            current_ssid(), self.offsets["x"], 0, font_adjust=3, upper_case=True
        )
        self.add_text(ipaddress, self.offsets["x"], 16, font_adjust=3)

    def boot(self):
        """Boot-time message."""
        self.set_image(self.width, self.height)

        # TODO: move these to a conf file?
        message = "booting"
        self.add_text(message, self.offsets["x"], self.offsets["y"])

    def reboot(self):
        """Reboot message."""
        self.set_image(self.width, self.height)

        # TODO: move these to a conf file?
        message = "rebooting"
        self.add_text(message, self.offsets["x"], self.offsets["y"])

    def reset(self):
        """Reset message."""
        self.set_image(self.width, self.height)

        message = "resetting"

        self.add_text(message, self.offsets["x"], self.offsets["y"])

    def wifi_switch(self):
        """Reload the wifi."""
        self.set_image(self.width, self.height)

        message = "switching wifi"

        self.add_text(message, self.offsets["x"], self.offsets["y"])

    def add_text(self, text, across, down, upper_case=False, font_adjust=None):  # noqa: FBT002, PLR0913
        """Add some text."""
        text = text.lower()
        if upper_case:
            text = text.upper()

        font = self.font
        if font_adjust:
            font = ImageFont.truetype(
                font=f"fonts/{self.conf['font']['name']}.ttf",
                size=self.conf["font"]["size"] - font_adjust,
            )

        self.draw.text((across, down), text, font=font, fill=255)

    def draw_brightness_bar(self):
        """Draw the brightness meter."""
        bar_width = 4
        step_size = 2
        max_height = self.height - 2
        count = int(max_height * self.custodian.get("brightness"))
        for i in range(0, count, step_size):
            for j in range(int(bar_width)):
                self.image.putpixel(
                    (self.width - (j + 2), (self.height - step_size) - i), 255
                )
            bar_width = bar_width + 1
