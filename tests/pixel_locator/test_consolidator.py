# from lib.pixel_locator import consolidate, find_highest_key


# def test_highest_key():
#     """Test it finds the highest key."""
#     assert find_highest_key({"a": {"0": {}}}) == 0
#     assert find_highest_key({"a": {"1": {}}}) == 1
#     assert find_highest_key({"a": {"1": {}}, "b": {"12": {}}}) == 12
#     assert find_highest_key({"a": {"1": {}}, "b": {"13": {}, "15": {}}}) == 15
#     assert find_highest_key({"a": {"25": {}}, "b": {"13": {}, "15": {}}}) == 25


# def test_consolidate_simple():
#     """Test the consolidator, simplest case."""
#     test_data = {
#         "front": {"000": {"x": 2, "y": 3}},
#     }
#     assert consolidate(test_data) == {"x": [2], "y": [3], "z": [None]}


# def test_consolidate_with_two_items():
#     """Test the consolidator, two simple items."""
#     test_data = {"front": {"000": {"x": 2, "y": 3}, "001": {"x": 4, "y": 5}}}
#     assert consolidate(test_data) == {"x": [2, 4], "y": [3, 5], "z": [None, None]}


# def test_consolidate_three_dimensions():
#     """Test the consolidator, with two aspects."""
#     test_data = {"front": {"000": {"x": 2, "y": 3}}, "right":
# {"000": {"x": 4, "y": 5}}}
#     assert consolidate(test_data) == {"x": [2], "y": [[3, 5]], "z": [4]}


# def test_consolidate_inversion():
#     """Test the consolidator, with an inverted aspect.."""
#     test_data = {"back": {"000": {"x": 2, "y": 3}}, "right":
# {"000": {"x": 4, "y": 5}}}
#     assert consolidate(test_data, pic_width=16) ==
# {"x": [14], "y": [[3, 5]], "z": [4]}
