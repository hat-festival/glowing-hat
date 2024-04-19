from signal import pause

from glowing_hat.controller import Controller


def manage():
    """Loop forever."""
    Controller()
    pause()


if __name__ == "__main__":
    manage()
