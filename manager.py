from signal import pause

from lib.controller import Controller


def manage():
    """Loop forever."""
    Controller()
    pause()


if __name__ == "__main__":
    manage()
