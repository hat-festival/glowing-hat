from pathlib import Path

import yaml

conf = yaml.safe_load(Path("conf/conf.yaml").read_text(encoding="UTF-8"))

exclusions = ["conf", "locations"]

for conf_file in filter(
    lambda x: x.stem not in exclusions, Path("conf").glob("*")
):
    conf[conf_file.stem] = yaml.safe_load(
        Path(conf_file).read_text(encoding="UTF-8")
    )
