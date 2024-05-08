from pathlib import Path

strings = sorted(Path("conf", "panel", "strings").glob("*.yaml"))


def load_strings(custodian):
    """Load the string-names into the Custodian."""
    custodian.unset("hoop:string")
    for string in strings:
        custodian.add_item_to_hoop(string.stem, "string")
