from colorsys import hsv_to_rgb
from pathlib import Path


def hue_to_rgb(hue):
    """Generate a GRB triple from a hue."""
    return list(map(lambda x: int(x * 255), hsv_to_rgb(hue, 1, 1)))  # noqa: C417


def close_enough(actual, target, tolerance=0.1):
    """Is a value close enough."""
    if abs(target - actual) <= tolerance:
        return True

    return False


def scale_colour(triple, factor):
    """Dim a colour."""
    return list(map(lambda x: int(x * factor), triple))  # noqa: C417


def remove_axis(axis):
    """Remove an axis from x, y, z."""
    return list(filter(lambda x: x != axis, ["x", "y", "z"]))


def colour_set_to_colour_list(colour_set, width):
    """Turn a colour-set definition into a list of RGB triples."""
    result = []
    for triple in list(colour_set.values()):
        for _ in range(width):
            result.append(triple)  # noqa: PERF401

    return result


def is_pi():
    """Detect if we're on a Pi."""
    model_file = "/sys/firmware/devicetree/base/model"
    return Path(model_file).exists() and "Raspberry Pi" in Path(model_file).read_text()
