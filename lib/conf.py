import os
from pathlib import Path

import yaml

CONF_PATH = os.environ.get("CONF_PATH", "conf")

conf = yaml.safe_load(Path(CONF_PATH, "conf.yaml").read_text(encoding="UTF-8"))

exclusions = ["conf", "locations"]

for conf_file in filter(lambda x: x.stem not in exclusions, Path("conf").glob("*")):
    conf[conf_file.stem] = yaml.safe_load(Path(conf_file).read_text(encoding="UTF-8"))

# for data in conf["modes"].values():
#     if "prefs" not in data:
#         data["prefs"] = conf["default-mode-prefs"]
