from glowing_hat.arrangements.word_streamer import WordIterator, as_bits


def test_as_bits():
    """Test it turns a character into columns of bits."""
    assert as_bits("a") == [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def test_bad_character():
    """Test it handles an unknown character."""
    assert as_bits("¡") == [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def test_string_as_bits():
    """Test it turns some characters into columns of bits."""
    assert as_bits("ab") == [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]


def test_word_iterator():
    """Test it yields string frames."""
    wi = WordIterator("abcd", 1)
    assert list(wi) == [" a", "ab", "bc", "cd", "d ", "  "]

    wi = WordIterator("abcdef", 3)
    assert list(wi) == [
        "   a",
        "  ab",
        " abc",
        "abcd",
        "bcde",
        "cdef",
        "def ",
        "ef  ",
        "f   ",
        "    ",
    ]
