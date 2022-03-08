# noqa

import signal
import sys

from RPi import GPIO


class ButtonTester:
    """Test buttons."""

    def got_button(self, button):
        """Bump to the next mode."""
        print(f"Button pressed: {button}")

    def signal_handler(self, _, __):
        """Handle a Ctrl-C etc."""
        GPIO.cleanup()
        sys.exit(0)

    def test(self):
        """Do the thing."""
        GPIO.setmode(GPIO.BCM)
        for pin in [23, 25, 12, 16]:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(
                pin,
                GPIO.FALLING,
                callback=lambda x: self.got_button(x),  # pylint:disable=W0108
                bouncetime=500,
            )

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.pause()


if __name__ == "__main__":
    but = ButtonTester()
    but.test()
