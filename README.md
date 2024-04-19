# Glowing Hat

_I glued 100 WS2812 NeoPixels to a hat then mapped them in 3D space_

https://user-images.githubusercontent.com/885973/168619388-2ef59b61-9f68-4e90-99ad-9d77b64aa226.mp4

## Construction

You will need:

- A [hard hat](https://www.ebay.co.uk/itm/262923531316)
- A [Pi Zero 2 W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/)
- A [button shim](https://thepihut.com/products/button-shim)
- An [OLED display](https://thepihut.com/products/adafruit-pioled-128x32-monochrome-oled-add-on-for-raspberry-pi-ada3527)
- 2 [NeoPixel strings](https://shop.pimoroni.com/products/rgb-led-wire?variant=31607418159187)
- A [USB Microphone](https://www.ebay.co.uk/itm/404669701943)
- A [USB OTG adapter](https://www.ebay.co.uk/itm/114893009469)
- A [power bank](https://www.ebay.co.uk/itm/133977636736)
- Wire
- Hot glue

I hot-glued the lights to the hat, turning in a random(ish) direction after I'd glued-down each one, attempting to move towards empty space each time. I also managed to stick 2 or 3 of them on backwards because I'm an idiot.

I cable-tied the Pi to the power-bank and wired everything up, producing something you absolutely would not want to try to take through an airport:

![not a bomb](assets/power-bank.jpg)

The data line is connected to [pin 21](lib/hat.py#L23) ([physical pin 40](https://pinout.xyz/pinout/pin40_gpio21)).

## Installing the software

From a box-fresh install of [64-bit Raspberry Pi Debian 12 (bookworm)](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-64-bit) (Note: I turned off device-filtering in the [Raspberry Pi imager](https://www.raspberrypi.com/software/) because it didn't want to let me have Bookworm for my Zero):

### Set hostname

```bash
sudo raspi-config nonint do_hostname glowing-hat
sudo reboot
```

### Install `git`

```bash
sudo apt --yes update && sudo apt install --no-install-recommends --yes git
```

### Get this repo

```bash
git clone https://github.com/hat-festival/glowing-hat
```

### Install everything

```bash
cd glowing-hat
./configure
make
```

## Mapping the lights

Once everything is assembled, you need to [take lots of photos](camera/README.md), and [do a load of analysis](analysis/README.md).

## Controls

The five buttons are are mapped as follows:

* A: cycle through the available `modes`
* B and C: turn the brightness up and down
* D: display the hat's IP address (if an Oled screen is available)
* E: _hold_ for one second to restart the `systemd` service
* A and D: _hold_ both of these for three seconds to reboot the whole Pi (sometimes things get really stuck)

## Modes

A [`mode`](lib/modes/cuttlefish.py) needs to inherit from [`Mode`](lib/mode.py), and should expose a [`run`](lib/modes/cuttlefish.py#L26) method, which loops forever and does something with the lights. A mode needs to be included in [this list](lib/modes_list.py) in order to be eligible, and then the mode ordering and per-mode preferences are defined [per hat](conf/glowing-hat/modes.yaml) - here, `glowing-hat` is the hostname to which this list will be applied.
