from hashlib import sha256
from pathlib import Path
from unittest import TestCase

import yaml
from mock import patch

from lib.custodian import Custodian
from lib.oled import ImageGenerator


class TestImageGenerator(TestCase):
    """Test the ImageGenerator."""

    def setUp(self):
        """Pre-test setup."""
        Path("tmp").mkdir(exist_ok=True)

        self.conf = yaml.safe_load(
            Path("tests", "fixtures", "image-generator", "conf.yaml").read_text(
                encoding="UTF-8"
            )
        )

        self.oled_conf = self.conf["oled"]
        self.cus = Custodian(namespace="test", conf=self.conf)
        self.cus.populate(flush=True)

        self.cus.rotate_until("axis", "y")
        self.cus.rotate_until("invert", False)
        self.cus.rotate_until("colour-source", "redis")
        self.cus.rotate_until("colour-set", "rgb")
        self.cus.rotate_until("colour", [255, 0, 0])
        self.cus.set("mode", "rotator")

    def test_hat_settings(self):
        """Test it generates the hat-settings screen."""
        self.cus.rotate_until("display-type", "hat-settings")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings")

        checksum = sha256(Path("tmp/hat-settings.png").read_bytes()).hexdigest()
        self.assertEqual(
            checksum, "8e17ae00b9fc4558a031c04bfe951a62c6dcd197e0b0ac6c1786939ecf91aee3"
        )

    def test_hat_settings_with_wheel(self):
        """Test it generates the hat-settings screen with the `wheel` colour-source."""
        self.cus.rotate_until("display-type", "hat-settings")
        self.cus.rotate_until("colour-source", "wheel")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="hat-settings")

        checksum = sha256(Path("tmp/hat-settings.png").read_bytes()).hexdigest()
        self.assertEqual(
            checksum, "713a43fadb28f9b406f3af3812d3082a9decaed94a97d7138e2fd81b0858bd45"
        )

    def test_button_config(self):
        """Test it generates the button-config screen."""
        self.cus.rotate_until("display-type", "button-config")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="button-config")

        checksum = sha256(Path("tmp/button-config.png").read_bytes()).hexdigest()
        self.assertEqual(
            checksum, "1f831d8afbe5b805d55bf39f32987d994d04be26f355d566701bb8d9bbb9b5ce"
        )

    @patch("socket.gethostname")
    @patch("socket.socket")
    def test_ip_address(self, mocked, mocked_method):
        """Test it generates the ip-address screen."""
        mocked.return_value.getsockname.return_value = ["192.168.168.111"]
        mocked_method.return_value = "testhost"

        self.cus.rotate_until("display-type", "ip-address")

        gen = ImageGenerator(self.cus, self.oled_conf)
        gen.generate(save_to="ip-address")

        checksum = sha256(Path("tmp/ip-address.png").read_bytes()).hexdigest()
        self.assertEqual(
            checksum, "e4fccb2d14ecdd921a8375688ef529e4f0de579dd23837fc7287060e19c43209"
        )
