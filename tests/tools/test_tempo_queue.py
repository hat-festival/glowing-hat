from glowing_hat.tools.tempo_queue import TempoQueue


def test_queue():
    """Test the queue."""
    tq = TempoQueue(2)
    assert list(tq.queue) == [0, 0]


def test_adding():
    """Test we can add things."""
    tq = TempoQueue(3)
    tq.add(1)
    tq.add(2)
    tq.add(3)

    assert (list(tq.queue)) == [3, 2, 1]


def test_rolling():
    """Test it's a FIFO."""
    tq = TempoQueue(2)
    tq.add(1)
    tq.add(2)
    tq.add(3)

    assert (list(tq.queue)) == [3, 2]


def test_averaging():
    """Test it can get the average interval."""
    tq = TempoQueue(4)
    tq.add(1.0)
    tq.add(2.0)
    tq.add(3.0)
    tq.add(4.0)

    assert tq.interval == 1.0


def test_trickier_average():
    """Test it can get the average interval."""
    tq = TempoQueue(6)
    tq.add(1)
    tq.add(2)
    tq.add(3)
    tq.add(4)
    tq.add(5)
    tq.add(6)
    tq.add(8)
    tq.add(10)
    tq.add(12)
    tq.add(14)
    tq.add(16)

    assert tq.interval == 2.0  # noqa: PLR2004
