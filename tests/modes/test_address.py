from glowing_hat.modes.address import address_to_bits


def test_bits():
    """Test it gets the right bits."""
    assert address_to_bits("192.168.68.111") == (
        "11000000",
        "10101000",
        "01000100",
        "01101111",
    )
