from signal import pause

from lib.control_manager import start


def manage():
    """Loop forever."""
    start()
    pause()


if __name__ == "__main__":
    manage()
