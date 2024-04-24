import contextlib
import platform
from collections import UserDict
from pathlib import Path

import yaml


class HatConf(UserDict):
    """Some conf."""

    def __init__(self, conf_root="conf"):
        """Construct."""
        self.conf_root = conf_root
        self.data = yaml.safe_load(
            Path(self.conf_root, "conf.yaml").read_text(encoding="UTF-8")
        )

        conf_path = Path(self.conf_root, platform.node(), "conf.yaml")
        if not conf_path.exists():
            conf_path = Path(self.conf_root, "glowing-hat", "conf.yaml")

        with contextlib.suppress(FileNotFoundError):
            self.per_hat_data = yaml.safe_load(conf_path.read_text(encoding="UTF-8"))
            self.data.update(self.per_hat_data)

        with contextlib.suppress(FileNotFoundError):
            self.data["modes"] = yaml.safe_load(
                Path(self.conf_root, platform.node(), "modes.yaml").read_text(
                    encoding="utf-8"
                )
            )


conf = HatConf()
