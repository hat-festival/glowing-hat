from random import choice, randint


# circle at a fixed altitude? I think this makes sense
def circle(axes, interval=0.1, direction="forwards"):
    """Get a set of keys to go round and round."""
    if direction == "backwards":
        axes = list(axes)
        axes.reverse()
        axes = tuple(axes)

    indeces = live_axes(axes)
    keys = [start_corner(axes)]

    for operation in operations:
        for index in indeces:
            for _ in range(-10, 10, int(interval * 10)):
                next_item = keys[-1].copy()
                next_item[index] = operation(next_item[index], interval)
                keys.append(next_item)

    keys.pop()

    return [as_key(x) for x in keys]


def random_step(current_step, step_size=0.1):
    """Get a (small) random step from where we are now."""
    vals = [float(x) for x in current_step[7:-1].split(",")]
    index = randint(0, 2)  # noqa: S311

    target = vals[index]
    if target == 1.0:
        target = decrement(target, step_size)
    elif target == -1.0:
        target = increment(target, step_size)
    else:
        target = choice(operations)(target, step_size)  # noqa: S311

    vals[index] = target
    # TODO abstract this out
    return as_key(vals)


def increment(value, amount):
    """Increment something."""
    return round(value + amount, 1)


def decrement(value, amount):
    """Decrement something."""
    return round(value - amount, 1)


def live_axes(axes):
    """Work out which axes are in play."""
    return ["xyz".index(axis) for axis in axes]


def start_corner(axes):
    """Work out the starting point."""
    point = []
    for char in "xyz":
        if char in axes:
            point.append(-1.0)
        else:
            point.append(0.0)

    return point


def as_key(data):
    """Turn a raw tuple into a Redis key."""
    return f"sorts:{tuple(data)}"


operations = [increment, decrement]
