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