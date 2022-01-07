from colorsys import hsv_to_rgb, rgb_to_hsv

from lib.gamma import gamma


def hue_to_grb(hue):
    """Generate a GRB triple from a hue."""
    rgb = list(map(lambda x: int(x * 255), hsv_to_rgb(hue, 1, 1)))
    return [rgb[1], rgb[0], rgb[2]]


def grb_to_hue(grb):
    """Convert a GRB triple to a hue value."""
    rgb = [grb[1], grb[0], grb[2]]
    return rgb_to_hsv(*list(map(lambda x: x / 255, rgb)))[0]


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return list(map(lambda n: gamma[n], triple))


def make_key(key, namespace):
    """Make compound key."""
    return f"{namespace}:{key}"
