import socket
from time import sleep

from glowing_hat.mode import Mode


class Address(Mode):
    """Show our IP address in binary."""

    def run(self):
        """Do the work."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ipaddress = sock.getsockname()[0]

        self.hat.off()

        while True:
            self.accumulator = 0
            self.draw_divider()

            for byte in address_to_bits(ipaddress):
                for bit in byte:
                    self.hat.apply_value_to_one_pixel(
                        self.accumulator, min(float(bit) + 0.2, 1)
                    )
                    self.accumulator += 1
                self.draw_divider()

            self.hat.light_up()

            sleep(0.1)


def address_to_bits(address):
    """IP address to binary."""
    return tuple(f"{int(byte):>08b}" for byte in address.split("."))
