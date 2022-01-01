from lib.tools import serial_ouput_to_grb


def test_serial_ouput_to_grb():
    """Test it parses the string correctly."""
    assert (serial_ouput_to_grb("(255, 19, 123)")) == [19, 255, 123]
