from colorsys import hsv_to_rgb

from lib.gamma import gamma


def hue_to_grb(hue):
    """Test it generates a GRB triple from a hue."""
    rgb = list(map(lambda x: int(x * 255), hsv_to_rgb(hue, 1, 1)))
    return [rgb[1], rgb[0], rgb[2]]


def gamma_correct(triple):
    """Gamma-correct a colour."""
    return list(map(lambda n: gamma[n], triple))
