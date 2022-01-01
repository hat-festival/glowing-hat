def serial_ouput_to_grb(binary):
    """Turn the serial output into a GRB triple."""
    rgb = list(map(int, binary[1:-1].split(", ")))
    return [rgb[1], rgb[0], rgb[2]]
