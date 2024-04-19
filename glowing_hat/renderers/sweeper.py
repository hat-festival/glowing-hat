# import pickle
# from math import atan2, degrees
# from pathlib import Path

# from glowing_hat.hat import Hat
# from glowing_hat.tools import remove_axis


# class Sweeper:
#     """Sweeper renderer."""

#     def __init__(self, hat=None):
#         """Construct."""
#         if hat:
#             self.hat = hat
#         else:
#             self.hat = Hat()

#     def render(self):
#         """Create some data."""
#         data = {}
#         for axis in ["x", "y", "z"]:
#             axis_0, axis_1 = remove_axis(axis)

#             for direction in ["f", "b"]:
#                 rev = False
#                 if direction == "b":
#                     rev = True

#                 data[f"{axis}-{direction}"] = self.populate(axis_0, axis_1, rev=rev)

#         Path("renders/sweeper.pickle").write_bytes(pickle.dumps(data))

#     def populate(self, axis_0, axis_1, step=1, rev=False):
#         """Populate ourself."""
#         frames = []
#         for angle in range(0, 360, step):
#             frames.append(self.make_frame(axis_0, axis_1, angle, rev=rev))

#         if not rev:
#             frames.reverse()

#         return frames

#     def make_frame(self, axis_0, axis_1, offset, rev=False):
#         """Make a single frame."""
#         frame = []
#         for pix in self.hat.pixels:
#             point_angle = (angle_to_point(pix[axis_0], pix[axis_1]) + offset) % 360

#             if rev:
#                 point_angle = 360 - point_angle

#             if point_angle == 0:
#                 point_angle = 360

#             factor = point_angle / 360

#             frame.append((pix["index"], factor))

#         return frame


# # https://stackoverflow.com/a/62482938
# def angle_to_point(axis_0, axis_1):
#     """Get the angle of this line with the horizontal axis."""
#     theta = atan2(axis_1, axis_0)
#     ang = degrees(theta)
#     if ang < 0:
#         ang = 360 + ang

#     if ang == 0:
#         ang = 360

#     return ang
