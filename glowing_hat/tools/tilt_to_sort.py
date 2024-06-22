from collections import OrderedDict

threshold = 5


def tilt_to_sort(x, y):
    """Turn tilt-values into a sort-key."""
    keys = OrderedDict({"x": 0.0, "y": 1.0, "z": 0.0})

    for pair in ((x, "z"), (y, "x")):
        match pair[0]:
            case foo if foo >= threshold:
                keys[pair[1]] = 1.0
            case foo if -threshold < foo < threshold:
                keys[pair[1]] = find_tilt(pair[0])
            case foo if foo <= -threshold:
                keys[pair[1]] = -1.0

    return tuple(keys.values())


def find_tilt(value):
    """Tilt for inside value."""
    return fix(round(value / threshold, 1))


def fix(value):
    """Suppress `-0.0`."""
    if value == -0.0:
        value = 0.0

    return value
