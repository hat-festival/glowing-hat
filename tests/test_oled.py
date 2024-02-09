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

    def test_hat_settings(self):
        """Test it generates the hat-settings screen."""
        self.cus.set("display-type", "hat-settings")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings")

        checksum = sha256(Path("tmp/hat-settings.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "15b87dd71eafa771fc8dc651b3cc2679eacef8086632a5c11af79e1116608bfd",
        )

    def test_hat_settings_with_wheel(self):
        """Test it generates the hat-settings screen with the `wheel` colour-source."""  # noqa: E501
        self.cus.set("display-type", "hat-settings")
        self.cus.set("colour-source", "wheel")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings-with-wheel")

        checksum = sha256(
            Path("tmp/hat-settings-with-wheel.png").read_bytes()
        ).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "d5df7c667430f066acfa5370f5393f6e6464d110b2db8cf6b91eb798ca63a058",
        )

    def test_hat_settings_with_no_axis(self):
        """Test it generates the hat-settings screen with no `axis` marker."""
        self.cus.set("mode", "pulsator")
        self.cus.set("display-type", "hat-settings")
        self.cus.set("colour-source", "wheel")
        self.cus.set("axis", "none")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings-no-axis")

        checksum = sha256(
            Path("tmp/hat-settings-no-axis.png").read_bytes()
        ).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "12ac0e23994b774583ab7f47ae2e8a46e3736bf3cbb922807421d9e9eb5ab240",
        )

    def test_hat_settings_with_invert(self):
        """Test it generates the hat-settings screen."""
        self.cus.set("display-type", "hat-settings")
        self.cus.set("invert", True)  # noqa: FBT003
        self.cus.set("axis", "x")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings-with-invert")

        checksum = sha256(
            Path("tmp/hat-settings-with-invert.png").read_bytes()
        ).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "83dcbc0f01651905874056224ac912d94abc54279f22f63fff174f574d9201e2",
        )

    def test_button_config(self):
        """Test it generates the button-config screen."""
        self.cus.set("display-type", "button-config")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="button-config")

        checksum = sha256(
            Path("tmp/button-config.png").read_bytes()
        ).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "46755679d44966c448c49a9f39b1fab279f23332b31a3421bf5b36e9be77ad2f",
        )

    def test_boot_screen(self):
        """Test it generates the boot-screen."""
        self.cus.set("display-type", "boot")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="boot")

        checksum = sha256(Path("tmp/boot.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "06fcc3e52988d996d43c6fb8eb9f983edfe4a858e35ae3766c914e0f24c9b148",
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
            "e4fccb2d14ecdd921a8375688ef529e4f0de579dd23837fc7287060e19c43209",
        )

    def test_get_sign(self):
        """Test it generates the correct sign."""
        gen = ImageGenerator(self.cus, self.oled_conf)

        self.cus.set("invert", False)  # noqa: FBT003
        self.assertEqual(gen.get_sign(), "+")  # noqa: PT009

        self.cus.set("invert", True)  # noqa: FBT003
        self.assertEqual(gen.get_sign(), "-")  # noqa: PT009
