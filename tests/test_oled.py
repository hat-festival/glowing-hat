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

        self.cus.set("axis", "y")
        self.cus.set("invert", False)  # noqa: FBT003
        self.cus.set("colour-source", "redis")
        self.cus.set("colour-set", "rgb")
        self.cus.set("colour", [255, 0, 0])
        self.cus.set("mode", "rotator")
        self.cus.set("brightness", 0.0)
        self.cus.set("fft-on", False)  # noqa: FBT003

    def test_hat_settings(self):
        """Test it generates the show-mode screen."""
        self.cus.set("display-type", "show-mode")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="show-mode")

        checksum = sha256(Path("tmp/show-mode.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "824f206e0d0f7372dc3be37cb5d9ee8c6d5eed339192c987c74095c2ad88bfe9",
        )

    def test_boot_screen(self):
        """Test it generates the boot-screen."""
        self.cus.set("display-type", "boot")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="boot")

        checksum = sha256(Path("tmp/boot.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "ec0c59e4f6476bedad734792e92969286f2aca14af4712ab1ee946ba831acfea",
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
            "13078980af2e141573c88eddaa84d2db024f5275abb08f2852df4b1694bafbd2",
        )

    def test_brightness_bar(self):
        """Test it generates the correct brightness bar."""
        self.cus.set("display-type", "show-mode")
        expectations = (
            (
                1.0,
                "b7a8c8a690a4e1e34ef3641b658f041fe13aef073ccecd91ca9ba9b780392e03",
            ),
            (
                0.5,
                "ecfd7b02ef717c106eaae0b6973fce9689d8f952220f6d4e3ab5fa7af98b44df",
            ),
            (
                0.1,
                "2717d5cf1fae89add3dacabb3f53275f477277ec8c9bf3a760bf6e7ae6be8c32",
            ),
            (
                0.0,
                "824f206e0d0f7372dc3be37cb5d9ee8c6d5eed339192c987c74095c2ad88bfe9",
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
                checksum, generated
            )
