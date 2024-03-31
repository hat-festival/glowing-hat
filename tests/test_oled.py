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
            "3f8fa825bed87234dd0c3cf4a8e1703f1d1a6385a894c2bb6e0633d618fd6e43",
        )

    def test_boot_screen(self):
        """Test it generates the boot-screen."""
        self.cus.set("display-type", "boot")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="boot")

        checksum = sha256(Path("tmp/boot.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "0f6c8013d499e4bde4bf5a881e7a495ad4002051c53600f4fe515cfd8c60d4c1",
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
            "ee75f82ad78abdf2e1c66aef90483b42966be13c5e7a10f4f194668f8d286be1",
        )

    def test_brightness_bar(self):
        """Test it generates the correct brightness bar."""
        self.cus.set("display-type", "show-mode")
        expectations = (
            (
                1.0,
                "5ac0a7a268eb7f237dfc0b095f988cdc6f36478ea382c08611360a7de84ca433",
            ),
            (
                0.5,
                "50d343980e35ad2142b6033519b3ff812672a1bf4d9da4acbb3eb7f078cdefad",
            ),
            (
                0.1,
                "b447358f6885182ab18246af3be9082b46ace0cf9cc95215f3c4d962f128466e",
            ),
            (
                0.0,
                "3f8fa825bed87234dd0c3cf4a8e1703f1d1a6385a894c2bb6e0633d618fd6e43",
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
