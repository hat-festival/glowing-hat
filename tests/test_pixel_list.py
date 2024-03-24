from lib.pixel_list import PixelList


def test_constructor():
    """Test it constructs."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations.yaml")

    assert pix_list[10].as_dict == {
        "index": 10,
        "x": -0.016029593094944512,
        "y": -0.3249075215782984,
        "z": 0.5043156596794082,
        "hue": 0.0,
        "rgb": (255, 0, 0),
        "saturation": 1.0,
        "value": 1.0,
        "angles": {
            "x": 122.79183214885639,
            "z": 267.17555335782856,
            "y": 358.1794756662044,
        },
    }


def test_rescaling():
    """Test we can trigger a full re-scale."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations.yaml")
    assert pix_list[99]["rgb"] == (255, 0, 0)

    pix_list.brightness_control.factor = 0.7
    pix_list.trigger_rescale()
    assert pix_list[99]["rgb"] == (93, 0, 0)


def test_lighting():
    """Test it lights up the lights."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations.yaml")
    for index, pixel in enumerate(pix_list):
        pixel["hue"] = index / 100

    assert pix_list[50]["hue"] == 0.5  # noqa: PLR2004
    assert pix_list[50]["rgb"] == (0, 255, 255)

    pix_list.light_up()
    assert pix_list.lights[60] == (0, 20, 255)
