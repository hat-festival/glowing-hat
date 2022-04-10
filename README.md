## Wiring

| Component   | Logical Pin | Physical Pin |
| ----------- | ----------- | ------------ |
| Lights Data | GPIO 21     | 40           |

## Set hostname and enable serial port

```bash
sudo raspi-config nonint do_hostname hatlights
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
