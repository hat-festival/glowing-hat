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
            "1439d1740ead7dd324cec13ce7d9406c603368759291bb6542b2963aaf78ef05",
        )

    def test_boot_screen(self):
        """Test it generates the boot-screen."""
        self.cus.set("display-type", "boot")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="boot")

        checksum = sha256(Path("tmp/boot.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "53d1f298e37f10bb218e70d81484de987265727ebb7ac00d44008a26597467ff",
        )

    @patch("subprocess.check_output")
    @patch("socket.socket")
    def test_ip_address(self, mocked, mocked_method):
        """Test it generates the ip-address screen."""
        mocked.return_value.getsockname.return_value = ["192.168.168.111"]
        mocked_method.return_value = b"GCHQ\nlo\n"

        self.cus.set("display-type", "ip-address")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="ip-address")

        checksum = sha256(Path("tmp/ip-address.png").read_bytes()).hexdigest()
        self.assertEqual(  # noqa: PT009
            checksum,
            "96382afe746ea88b24ebaa5441a07ce207a9eff684841052e4e09af0ebda7d1e",
        )

    def test_brightness_bar(self):
        """Test it generates the correct brightness bar."""
        self.cus.set("display-type", "show-mode")
        expectations = (
            (
                1.0,
                "5b8efb713c806876da94cfdfe9653715f3b814ac56bb589f340a5ad6a0a1303d",
            ),
            (
                0.5,
                "d800fa77430878ab6f564a4c3e549ef70cbfca60d25ffaf84e4c079042c9f25d",
            ),
            (
                0.1,
                "c95f691b79627576b052274af36d5459ce4a4b66555e1dfaeb07a6a9612dbc14",
            ),
            (
                0.0,
                "1439d1740ead7dd324cec13ce7d9406c603368759291bb6542b2963aaf78ef05",
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
