from hashlib import sha256
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from lib.conf import conf
from lib.custodian import Custodian
from lib.oled import ImageGenerator


class TestImageGenerator(TestCase):
    """Test the ImageGenerator."""

    def setUp(self):
        """Pre-test setup."""
        Path("tmp").mkdir(exist_ok=True)

        self.conf = conf

        self.oled_conf = self.conf["oled"]
        self.cus = Custodian(namespace="test", conf=self.conf)
        self.cus.populate(flush=True)

        self.cus.set("mode", "brainwaves")
        self.cus.set("brightness", 0.0)

    def test_hat_settings(self):
        """Test it generates the show-mode screen."""
        self.cus.set("display-type", "show-mode")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="show-mode")

        checksum = sha256(Path("tmp/show-mode.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "9a534ddce6645291ca589409e3bca80c9b771dcc9ac8fc320be5c2960a1e40ce",
        )

    def test_boot_screen(self):
        """Test it generates the boot-screen."""
        self.cus.set("display-type", "boot")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="boot")

        checksum = sha256(Path("tmp/boot.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "909b98b2028d9b7d70071eea538d2c97ba0e067bcb9668683b50b283a8852266",
        )

    @patch("socket.gethostname")
    @patch("socket.socket")
    def test_ip_address(self, mocked, mocked_method):
        """Test it generates the ip-address screen."""
        mocked.return_value.getsockname.return_value = ["192.168.168.111"]
        mocked_method.return_value = "testhost"

        self.cus.set("display-type", "ip-address")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="ip-address")

        checksum = sha256(Path("tmp/ip-address.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "2e5cd1badf53fe5d8742d64b56261e5ba3a791ec3e06dd75b061a9b9a8ca089b",
        )

    def test_brightness_bar(self):
        """Test it generates the correct brightness bar."""
        self.cus.set("display-type", "show-mode")
        expectations = (
            (
                1.0,
                "cbd5c1918f8da381d7762cf541aaca280200060873f1a9101ba63cc3f9474d50",
            ),
            (
                0.5,
                "0f735146962a60866e51e8cff44daa172c14d794454b52c1f671691d2a5656ab",
            ),
            (
                0.1,
                "add71c07d42ab645148f0203f89a66d40ffd6358911b9dcb0a5a6a6177444488",
            ),
            (
                0.0,
                "9a534ddce6645291ca589409e3bca80c9b771dcc9ac8fc320be5c2960a1e40ce",
            ),
        )

        for brightness, checksum in expectations:
            self.cus.set("brightness", brightness)
            gen = ImageGenerator(self.cus, self.oled_conf)
            gen.generate(save_to=f"brightness-bar-{brightness}")

            generated = sha256(
                Path(f"tmp/brightness-bar-{brightness}.png").read_bytes()
            ).hexdigest()
            self.assertEqual(  # noqa: PT009
                generated,
                checksum,
            )
