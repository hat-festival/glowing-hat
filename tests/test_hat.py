# from unittest import TestCase
# from unittest.mock import patch

# from lib.conf import conf
# from lib.hat import Hat


# @patch.dict(conf, {"brightness-factor": 1.0})
# class TestHat(TestCase):
#     """Test the Hat."""

#     def setUp(self):
#         self.hat = Hat(locations="tests/fixtures/hat/locations.yaml")

#     def test_init(self):
#         """Test it gets the correct data."""
#         self.assertEqual(self.hat.pixels[0]["index"], 0)
#         self.assertEqual(self.hat.pixels[97]["index"], 97)

#     def test_light_one(self):
#         """Test it lights a light."""
#         self.hat.light_one(8, [255, 0, 0])

#         self.assertEqual(
#             self.hat.lights[0:9],
#             [
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (127, 0, 0),
#             ],
#         )

#     def test_colour_indeces(self):
#         """Test it lights a bunch of lights."""
#         self.hat.colour_indeces([0, 7, 4], [0, 255, 0])
#         self.hat.colour_indeces([3, 5], [0, 0, 255])

#         self.assertEqual(
#             self.hat.lights[0:9],
#             [
#                 (0, 127, 0),
#                 (0, 0, 0),
#                 (0, 0, 0),
#                 (0, 0, 127),
#                 (0, 127, 0),
#                 (0, 0, 127),
#                 (0, 0, 0),
#                 (0, 127, 0),
#                 (0, 0, 0),
#             ],
#         )

#     def test_hat_sorting(self):
#         """Test sorting the hat along an axis."""
#         self.hat.sort("x")

#         self.assertEqual(
#             list(map(lambda x: x["index"], self.hat.pixels))[0:16],
#             [50, 12, 70, 85, 77, 5, 11, 24, 91, 25, 84, 78, 63, 30, 62, 36],
#         )
#         for i in range(len(self.hat.pixels) - 1):
#             self.assertLessEqual(
#                 self.hat.pixels[i]["x"], self.hat.pixels[i + 1]["x"]
#             )

#     def test_illuminate(self):
#         """Test it applies a whole set of colours."""
#         # create list from `[255, 0, 0]` down to `[156, 0, 0]`
#         colours = []
#         for i in range(255, 155, -1):
#             colours.append([i, 0, 0])

#         self.hat.sort("x")
#         self.hat.illuminate(colours)

#         self.assertEqual(self.hat.lights[50], (127, 0, 0))
#         self.assertEqual(self.hat.lights[12], (126, 0, 0))
#         self.assertEqual(self.hat.lights[62], (109, 0, 0))
#         self.assertEqual(self.hat.lights[36], (107, 0, 0))
