from pathlib import Path

import yaml

strings = yaml.safe_load(
    Path("conf", "panel", "strings.yaml").read_text(encoding="utf-8")
)


def load_strings(custodian):
    """Load the string-names into the Custodian."""
    custodian.unset("hoop:string")
    for string in strings:
        custodian.add_item_to_hoop(string, "string")
