from unittest import TestCase

from lib.pixel_locator import PixelLocator, average_out, scale

# class TestPixelLocator(TestCase):
#     """Test the PixelLocator."""

#     def test_consolidate(self):
#         """Test it consolidates the data."""
#         ploc = PixelLocator([720, 480], data_root="tests/fixtures/analysis", lights=20)
#         self.assertEqual(
#             ploc.consolidated_data,
#             {
#                 "x": [
#                     347,
#                     544,
#                     445,
#                     445,
#                     193,
#                     93,
#                     171,
#                     496,
#                     496,
#                     615,
#                     332,
#                     111,
#                     111,
#                     175,
#                     447,
#                     447,
#                     570,
#                     252,
#                     252,
#                     414,
#                 ],
#                 "y": [
#                     [391, 340],
#                     [220, 177],
#                     [38, 54],
#                     [38, 86],
#                     [97, 72],
#                     [143, 157],
#                     [176, 246],
#                     [131, 116],
#                     [131, 204],
#                     [281, 284],
#                     [296, 284],
#                     [293, 271],
#                     [293, 297],
#                     [76, 149],
#                     [49, 33],
#                     [49, 140],
#                     [223, 236],
#                     [117, 136],
#                     [117, 19],
#                     [31, 11],
#                 ],
#                 "z": [
#                     93,
#                     59,
#                     324,
#                     529,
#                     555,
#                     287,
#                     112,
#                     77,
#                     266,
#                     565,
#                     565,
#                     626,
#                     295,
#                     162,
#                     180,
#                     361,
#                     593,
#                     658,
#                     448,
#                     241,
#                 ],
#             },
#         )

#     def test_flattening(self):
#         """Test it averages-out the data."""
#         ploc = PixelLocator([720, 480], data_root="tests/fixtures/analysis", lights=20)
#         self.assertEqual(
#             ploc.flattened_data,
#             {
#                 "x": [
#                     347.0,
#                     544.0,
#                     445.0,
#                     445.0,
#                     193.0,
#                     93.0,
#                     171.0,
#                     496.0,
#                     496.0,
#                     615.0,
#                     332.0,
#                     111.0,
#                     111.0,
#                     175.0,
#                     447.0,
#                     447.0,
#                     570.0,
#                     252.0,
#                     252.0,
#                     414.0,
#                 ],
#                 "y": [
#                     365.5,
#                     198.5,
#                     46.0,
#                     62.0,
#                     84.5,
#                     150.0,
#                     211.0,
#                     123.5,
#                     167.5,
#                     282.5,
#                     290.0,
#                     282.0,
#                     295.0,
#                     112.5,
#                     41.0,
#                     94.5,
#                     229.5,
#                     126.5,
#                     68.0,
#                     21.0,
#                 ],
#                 "z": [
#                     93.0,
#                     59.0,
#                     324.0,
#                     529.0,
#                     555.0,
#                     287.0,
#                     112.0,
#                     77.0,
#                     266.0,
#                     565.0,
#                     565.0,
#                     626.0,
#                     295.0,
#                     162.0,
#                     180.0,
#                     361.0,
#                     593.0,
#                     658.0,
#                     448.0,
#                     241.0,
#                 ],
#             },
#         )

#     def test_limits(self):
#         """ "Test it finds the mins and maxes."""
#         ploc = PixelLocator([720, 480], data_root="tests/fixtures/analysis", lights=20)
#         self.assertEqual(
#             ploc.limits,
#             {
#                 "x": {"max": 615.0, "min": 93.0},
#                 "y": {"max": 365.5, "min": 21.0},
#                 "z": {"max": 658.0, "min": 59.0},
#             },
#         )


def test_scale():
    """Test it scales some items."""
    cases = (
        ([1, 2], [-1, 1]),
        ([0, 1, 2], [-1, 0, 1]),
        ([0, 2, 4], [-1, 0, 1]),
        ([1, 2, 3], [-1, 0, 1]),
        ([0, 1, 2, 3, 4, 8], [-1.0, -0.75, -0.5, -0.25, 0.0, 1.0]),
        ([4, 2, 3, 8, 0, 1], [0.0, -0.5, -0.25, 1.0, -1.0, -0.75]),
    )

    for items, expected in cases:
        assert scale(items) == expected

    more_cases = (
        ([1, 2], 1, [-1, 1]),
        ([1, 2], 2, [-2, 2]),
        ([1, 2], 0.5, [-0.5, 0.5]),
        ([0, 1, 2, 3, 4, 8], 2, [-2.0, -1.5, -1.0, -0.5, 0.0, 2.0]),
        ([0, 1, 2, 3, 4, 8], 0.5, [-0.5, -0.375, -0.25, -0.125, 0.0, 0.5]),
    )
    for items, factor, expected in more_cases:
        assert scale(items, factor) == expected


def test_average_out():
    """Test it averages a list."""
    assert average_out([1]) == 1
    assert average_out([1, 3]) == 2
    assert average_out([1, 4]) == 2.5
