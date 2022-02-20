from lib.pixel_locator import flatten, flatten_list


def test_flatten_list():
    """Test it flattens a list."""
    assert flatten_list([1, 2, 3]) == [1, 2, 3]
    assert flatten_list([1, [2, 4], 5]) == [1, 3, 5]


def test_flatten():
    """Test it flattens a dataset."""
    test_data = {
        "x": [1, 5, 7, 3, 5],
        "y": [19, [22, 17], 12, 200, 3],
        "z": [4, 3, 5, [6, 8], 10],
    }

    assert flatten(test_data) == {
        "x": [1.0, 5.0, 7.0, 3.0, 5.0],
        "y": [19.0, 19.5, 12.0, 200.0, 3.0],
        "z": [4.0, 3.0, 5.0, 7.0, 10.0],
    }
