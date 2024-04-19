from unittest.mock import patch

from glowing_hat.arrangements.riser_list import RiserList


@patch("glowing_hat.arrangements.riser_list.random")
def test_easy_case(mock_random):
    """Test the simple case."""
    mock_random.return_value = 0.5
    rl = RiserList(10)
    assert rl.data == [
        "primary",
        "primary",
        "primary",
        "primary",
        "primary",
        "secondary",
        "secondary",
        "secondary",
        "secondary",
        "secondary",
    ]
