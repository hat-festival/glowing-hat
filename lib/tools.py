from colorsys import hsv_to_rgb

from lib.gamma import gamma


def hue_to_rgb(hue):
    """Generate a GRB triple from a hue."""
    return list(map(lambda x: int(x * 255), hsv_to_rgb(hue, 1, 1)))


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return list(map(lambda n: gamma[n], triple))


def make_key(key, namespace):
    """Make compound key."""
    return f"{namespace}:{key}"


def close_enough(actual, target, tolerance=0.1):
    """Is a value close enough."""
    if abs(target - actual) <= tolerance:
        return True

    return False


def scale_colour(triple, factor):
    """Dim a colour."""
    return list(map(lambda x: int(x * factor), triple))


def remove_axis(axis):
    """Remove an axis from x, y, z."""
    return list(filter(lambda x: x != axis, ["x", "y", "z"]))
