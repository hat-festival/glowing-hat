from pathlib import Path

import yaml

conf = yaml.safe_load(Path("conf/conf.yaml").read_text(encoding="UTF-8"))
