from glowing_hat.tools.tilt_to_sort import tilt_to_sort

assert tilt_to_sort(0.0, 0.0) == (0.0, 1.0, 0.0)

assert tilt_to_sort(10.0, 0) == (0.0, 1.0, 1.0)
assert tilt_to_sort(5.0, 0) == (0.0, 1.0, 1.0)
assert tilt_to_sort(-5.0, 0) == (0.0, 1.0, -1.0)
assert tilt_to_sort(-10.0, 0) == (0.0, 1.0, -1.0)

assert tilt_to_sort(4.0, 0) == (0.0, 1.0, 0.8)
assert tilt_to_sort(-4.0, 0) == (0.0, 1.0, -0.8)

assert tilt_to_sort(0, 4.0) == (0.8, 1.0, 0.0)
assert tilt_to_sort(0, -4.0) == (-0.8, 1.0, 0.0)
