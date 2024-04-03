from lib.arrangements.rolling_queue import RollingQueue


def test_constructor():
    """Test it sets up right."""
    rq = RollingQueue(length=3)
    assert rq == [None, None, None]


def test_adding_items():
    """Test we can add things."""
    rq = RollingQueue(length=3)
    rq.push("a")
    assert rq == [None, None, "a"]

    rq.push("b")
    rq.push("c")
    assert rq == ["a", "b", "c"]


def test_longer_queue():
    """Test for more items."""
    rq = RollingQueue(length=5)
    rq.push("i")
    rq.push("j")
    rq.push("k")
    rq.push("l")
    assert rq == [None, "i", "j", "k", "l"]


def test_length_is_retained():
    """Test things fall off the end."""
    rq = RollingQueue(length=3)
    for i in range(25):
        rq.push(i)

    assert rq == [22, 23, 24]


def test_a_queue_of_one():
    """Test it handles a single-item queue."""
    rq = RollingQueue(length=1)
    assert rq == [None]

    rq.push("a")
    rq.push("b")
    assert rq == ["b"]
