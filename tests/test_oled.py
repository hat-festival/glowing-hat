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
        """Test it generates the hat-settings screen."""
        self.cus.set("display-type", "hat-settings")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings")

        checksum = sha256(Path("tmp/hat-settings.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "0820629812d9a0645eb134d8d0d5aeed67e103977eeb0b3947d3f775eb2a072c",
        )

    def test_hat_settings_with_wheel(self):
        """Test it generates the hat-settings screen with the `wheel` colour-source."""
        self.cus.set("display-type", "hat-settings")
        self.cus.set("colour-source", "wheel")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings-with-wheel")

        checksum = sha256(
            Path("tmp/hat-settings-with-wheel.png").read_bytes()
        ).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "a4bf8b66bc66a1a4625fa368912e6e71a9ab5750693ed74f320147ae1b23af48",
        )

    def test_hat_settings_with_no_axis(self):
        """Test it generates the hat-settings screen with no `axis` marker."""
        self.cus.set("mode", "pulsator")
        self.cus.set("display-type", "hat-settings")
        self.cus.set("colour-source", "wheel")
        self.cus.set("axis", "none")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings-no-axis")

        checksum = sha256(Path("tmp/hat-settings-no-axis.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "4bf1fd099e69fafb8570a1bbfca86ec805b8b05a18236d3deeea35a642275ac7",
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
            "17ceb94646b096e9ad11d14ee80cbd14ac7c542fdca4e49328744d782ed68b81",
        )

    def test_button_config(self):
        """Test it generates the button-config screen."""
        self.cus.set("display-type", "button-config")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="button-config")

        checksum = sha256(Path("tmp/button-config.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "e632f04f8b86fd36eb9eb09f57f30e4fee84aae1a8d943ef2729880f6d0ca58a",
        )

    def test_boot_screen(self):
        """Test it generates the boot-screen."""
        self.cus.set("display-type", "boot")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="boot")

        checksum = sha256(Path("tmp/boot.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "c82f8ad6b6123c8963d2af05af63cbdfadf78b8f1579f97caea379429db4d853",
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
            "bb50d7df95fdd527693c4a7eaa966cfbe36cc12476588cfe2d8b50e8eaf15079",
        )

    def test_get_sign(self):
        """Test it generates the correct sign."""
        gen = ImageGenerator(self.cus, self.oled_conf)

        self.cus.set("invert", False)  # noqa: FBT003
        self.assertEqual(gen.get_sign(), "+")  # noqa: PT009

        self.cus.set("invert", True)  # noqa: FBT003
        self.assertEqual(gen.get_sign(), "-")  # noqa: PT009

    def test_brightness_bar(self):
        """Test it generates the correct brightness bar."""
        expectations = (
            (
                1.0,
                "c35c579cae7cb6fbf262cee3edd2b85dda0749dfd98966e56145266000678e0c",
            ),
            (
                0.5,
                "8c96cef5fbcf04ca30b1e1299a090cded55ca30eb5a4a88fedec2b2cebb374b9",
            ),
            (
                0.1,
                "214f89d4fabf118f29085faabf520c3bd535ca85ec4393699e2961c67c7e7927",
            ),
            (
                0.0,
                "0820629812d9a0645eb134d8d0d5aeed67e103977eeb0b3947d3f775eb2a072c",
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

    def test_with_fft_symbol(self):
        """Test it generates a little musical note when we are FFTing."""
        self.cus.set("fft-on", True)  # noqa: FBT003
        self.cus.set("brightness", 0.0)
        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="with-fft")
        checksum = sha256(Path("tmp/with-fft.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "e9cdee8166d47e19b3b528192b915ea45a6b27540beeaf6ca164f5a626503a90",
        )
