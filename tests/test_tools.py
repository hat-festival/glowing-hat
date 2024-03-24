from lib.pixel import Pixel
from lib.tools import (
    brighten_pixels_less_than_y,
    close_enough,
    colour_set_to_colour_list,
    hue_to_rgb,
    remove_axis,
    scale_colour,
)
from tests.fixtures.equaliser_data.expectations import equaliser_data


def test_hue_to_rgb():
    """Test it turns a `hue` value into an RGB triple."""
    cases = (
        (0, [255, 0, 0]),
        (0.5, [0, 255, 255]),
    )

    for hue, rgb in cases:
        assert hue_to_rgb(hue) == rgb


def test_close_enough():
    """Test it knows if a thing is close enough."""
    assert close_enough(0.01, 0)
    assert close_enough(0.05, 0)
    assert not close_enough(0.1, 0, tolerance=0.05)
    assert close_enough(0.51, 0.5)
    assert close_enough(0.49, 0.5)
    assert close_enough(0.44, 0.5)
    assert close_enough(-0.51, -0.5)
    assert not close_enough(-0.44, -0.5, tolerance=0.01)


def test_scale_colour():
    """Test it scales a colour."""
    assert scale_colour([255, 0, 127], 0.5) == [127, 0, 63]


def test_remove_axis():
    """Test it removes the axis."""
    assert remove_axis("x") == ["y", "z"]
    assert remove_axis("y") == ["x", "z"]
    assert remove_axis("z") == ["x", "y"]


def test_colour_set_to_colour_list():
    """Test it transforms the colours."""
    colour_set = {
        "red": [255, 0, 0],
        "yellow": [255, 255, 0],
        "green": [0, 255, 0],
        "cyan": [0, 255, 255],
        "blue": [0, 0, 255],
        "magenta": [255, 0, 255],
    }
    assert colour_set_to_colour_list(colour_set, 2) == [
        [255, 0, 0],
        [255, 0, 0],
        [255, 255, 0],
        [255, 255, 0],
        [0, 255, 0],
        [0, 255, 0],
        [0, 255, 255],
        [0, 255, 255],
        [0, 0, 255],
        [0, 0, 255],
        [255, 0, 255],
        [255, 0, 255],
    ]


def test_brighten_pixels_less_than_y():
    """Test it dims the correct pixels."""
    pixels = [Pixel(real_data) for real_data in equaliser_data["pixels"]]

    # for index, hue in enumerate(equaliser_data["hues"]):
    #     pixels[index]["hue"] = hue

    # for index, y in enumerate(equaliser_data["ys"]):
    #     pixels[index]["y"] = y

    assert (
        brighten_pixels_less_than_y(
            pixels, equaliser_data["active-y"], equaliser_data["scale-factor"]
        )
        == equaliser_data["colours"]
    )
