def circle(axes, interval=0.1):  # , direction="forwards"):
    """Get a set of keys to go round and round."""
    keys = [start_corner(axes)]

    if "z" in axes:
        count = 0
        while count <= 1:
            keys.append((keys[-1][0], keys[-1][1], keys[-1][2] + interval))
            count += interval

    if "x" in axes:
        count = 0
        while count <= 1:
            keys.append((keys[-1][0] + interval, keys[-1][1], keys[-1][2]))
            count += interval

    if "z" in axes:
        count = 1
        while count >= 0:
            keys.append((keys[-1][0], keys[-1][1], keys[-1][2] - interval))
            count -= interval

    if "x" in axes:
        count = 1
        while count > 0:
            keys.append((keys[-1][0] - interval, keys[-1][1], keys[-1][2]))
            count -= interval

    return [f"sorts:{x}" for x in keys]


def start_corner(axes):
    """Work out the starting point."""
    point = [0.0, 0.0, 0.0]
    if "x" in axes:
        point[0] = -1.0

    if "y" in axes:
        point[1] = -1.0

    if "z" in axes:
        point[2] = -1.0

    return tuple(point)
