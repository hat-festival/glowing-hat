from lib.pixel_locator import flatten_list

def test_flatten_list():
    """Test it flattens a list."""
    assert flatten_list([1, 2, 3]) == [1, 2, 3]
    assert flatten_list([1, [2, 4], 5]) == [1, 3, 5]
