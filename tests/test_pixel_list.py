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
        "saturation": 1.0,
        "value": 1.0,
        "angles": {
            "x": 122.79183214885639,
            "z": 267.17555335782856,
            "y": 358.1794756662044,
        },
    }


def test_lighting():
    """Test it lights up the lights."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations.yaml")
    for index, pixel in enumerate(pix_list):
        pixel["hue"] = index / 100

    assert pix_list[50]["hue"] == 0.5  # noqa: PLR2004

    pix_list.light_up()
    assert pix_list.lights[60] == (0, 20, 255)


def test_sorting_by_indeces():
    """Test we can order ourself by some arbitrary indeces."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    pix_list[0]["hue"] = 0.5
    pix_list.sort_by_indeces([4, 2, 1, 3, 0])

    assert pix_list[4]["hue"] == 0.5  # noqa: PLR2004
    assert [pixel["index"] for pixel in pix_list] == [4, 2, 1, 3, 0]
