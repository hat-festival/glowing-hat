## Wiring

| Component             | Logical Pin | Physical Pin |
| --------------------- | ----------- | ------------ |
| Lights Data           | GPIO 18     | 12           |
| Lights Ground         | GND         | 6            |
| Wheel-control button  | GPIO 17     | 11           |
| Colour-stepper button | GPIO 23     | 16           |
| Mode button           | GPIO 25     | 22           |

## Set hostname and enable serial port

```bash
sudo raspi-config nonint do_hostname hatlights
sudo raspi-config nonint do_serial 1
sudo reboot
```

## Install `git`

```bash
sudo apt -y update && sudo apt install -y git
```

## Get this repo

```bash
git clone https://github.com/hat-festival/hatlights
cd hatlights
```

## Configure everything

```bash
./configure
make
```
