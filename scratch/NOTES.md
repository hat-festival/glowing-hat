# Serial port fuckery

- Enable serial port `raspi-config nonint do_serial 1` (this also enables a login shell on the serial port, I don't think we care)

## Pins

| Camera | Pi       |
| ------ | -------- |
| 4 (TX) | 10 (RX)  |
| 5 (RX) | 8 (TX)   |
| GND    | 39 (GND) |

## Code

Camera:

```python
import sensor, image, time
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()
uart = UART(3, 19200, timeout_char=1000)

while(True):
    clock.tick()
    img = sensor.snapshot()
    stats = img.get_statistics()
    rgb = f"{str(image.lab_to_rgb([stats.l_mean(), stats.a_mean(), stats.b_mean()]))}\r"
    uart.write(rgb)

    time.sleep(1)
```

Pi:

```python
import time
import serial
import io
from lib.light_string import LightString
ls = LightString()

ser = serial.Serial(
  port='/dev/serial0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
  baudrate = 19200,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

buf = ''
while 1:
  character = ser.read().decode()
  if character == "\r":
    rgb = list(map(int, buf[1:-1].split(', ')))
    rgb = [rgb[1], rgb[0], rgb[2]]
    print(rgb)
    ls.light_all(rgb)

    buf = ''
  else:
    buf += character

  time.sleep(0.1)
```
