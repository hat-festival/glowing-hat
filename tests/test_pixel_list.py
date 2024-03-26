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


def test_applying_hues():
    """Test we can apply a list of hues to ourself."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    hues = [0.1, 1.0, 0.34, 0.55, 0.02]

    pix_list.apply_hues(hues)
    assert [pixel["hue"] for pixel in pix_list] == [0.1, 1.0, 0.34, 0.55, 0.02]


def test_applying_values():
    """Test we can apply a list of hues to ourself."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    values = [0.02, 0.55, 0.34, 1.0, 0.1]

    pix_list.apply_values(values)
    assert [pixel["value"] for pixel in pix_list] == [0.02, 0.55, 0.34, 1.0, 0.1]


def test_updating_hues_from_angles():
    """Test we can update our hues-from-angles."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    assert [pixel["angles"]["y"] for pixel in pix_list] == [
        360,
        356.4236656250026,
        266.4236656250026,
        176.42366562500266,
        86.42366562500266,
    ]
    assert [pixel["hue"] for pixel in pix_list] == [0.0, 0.0, 0.0, 0.0, 0.0]

    pix_list.update_hues_from_angles(offset=45)
    assert [pixel["hue"] for pixel in pix_list] == [
        0.125,
        0.11506573784722952,
        0.8650657378472295,
        0.6150657378472296,
        0.3650657378472296,
    ]


def test_applying_hue():
    """Test we can apply one hue to all the pixels."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    assert [pixel["hue"] for pixel in pix_list] == [0.0, 0.0, 0.0, 0.0, 0.0]

    pix_list.apply_hue(0.2)
    assert [pixel["hue"] for pixel in pix_list] == [0.2, 0.2, 0.2, 0.2, 0.2]


def test_applying_value():
    """Test we can apply one value to all the pixels."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    assert [pixel["value"] for pixel in pix_list] == [1.0, 1.0, 1.0, 1.0, 1.0]

    pix_list.apply_value(0.75)
    assert [pixel["value"] for pixel in pix_list] == [0.75, 0.75, 0.75, 0.75, 0.75]


def test_dimming_pixels_greater_than_foo():
    """Test we can dim some pixels."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    assert [pixel["value"] for pixel in pix_list] == [1.0, 1.0, 1.0, 1.0, 1.0]

    pix_list.dim_pixels_greater_than_foo(0.1, 0.2)
    assert [pixel["value"] for pixel in pix_list] == [0.1, 1.0, 1.0, 1.0, 1.0]


def test_we_support_len():
    """Test out list supports `len()`."""
    pix_list = PixelList(locations="tests/fixtures/hat/locations/simple.yaml")
    assert len(pix_list) == 5  # noqa: PLR2004
